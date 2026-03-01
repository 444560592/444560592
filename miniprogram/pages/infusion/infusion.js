// pages/infusion/infusion.js — 输液计时器
//
// Timer state uses an "adjusted start" approach so pause/resume works correctly:
//   adjustedStart = Date.now() - bagElapsed * 1000
//   elapsed       = Math.floor((Date.now() - adjustedStart) / 1000)
// On pause:  bagElapsed = elapsed
// On resume: adjustedStart = Date.now() - bagElapsed * 1000

const app = getApp();

let _tick = null;

function getElapsed(data) {
  if (data.phase === 'running') {
    return Math.floor((Date.now() - data.adjustedStart) / 1000);
  }
  return data.bagElapsed;
}

Page({
  data: {
    // Config
    bagCount:       1,
    minutesPerBag:  60,
    // Runtime state
    phase:          'config',   // config | running | paused | done
    currentBag:     1,
    bags:           [{ n: 1, done: false, active: true }],
    adjustedStart:  0,
    bagElapsed:     0,
    // Display
    displayTime:    '60:00',
    progress:       0,
  },

  onLoad()    { this._restore(); },
  onShow()    { if (this.data.phase === 'running') this._startTick(); },
  onHide()    { this._stopTick(); },
  onUnload()  { this._stopTick(); },

  // ── Persistence ─────────────────────────────────────────────────────────
  _restore() {
    const s = app.globalData.infusionState;
    if (!s || s.phase === 'config' || s.phase === 'done') return;
    this.setData({ ...s });
    this._updateDisp(getElapsed(s), s.minutesPerBag * 60);
    if (s.phase === 'running') this._startTick();
  },

  _save() {
    app.globalData.infusionState = {
      bagCount:      this.data.bagCount,
      minutesPerBag: this.data.minutesPerBag,
      phase:         this.data.phase,
      currentBag:    this.data.currentBag,
      bags:          this.data.bags,
      adjustedStart: this.data.adjustedStart,
      bagElapsed:    this.data.bagElapsed,
    };
  },

  // ── Tick ────────────────────────────────────────────────────────────────
  _startTick() {
    if (_tick) clearInterval(_tick);
    _tick = setInterval(() => this._onTick(), 1000);
  },

  _stopTick() {
    if (_tick) { clearInterval(_tick); _tick = null; }
  },

  _onTick() {
    const el    = getElapsed(this.data);
    const total = this.data.minutesPerBag * 60;
    if (el >= total) { this._onBagDone(); return; }
    this._updateDisp(el, total);
  },

  _updateDisp(el, total) {
    const rem = Math.max(0, total - el);
    const mm  = Math.floor(rem / 60);
    const ss  = rem % 60;
    this.setData({
      displayTime: `${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`,
      progress:    Math.min(100, Math.round(el / total * 100)),
    });
  },

  // ── Bag lifecycle ────────────────────────────────────────────────────────
  _onBagDone() {
    this._stopTick();
    wx.vibrateLong();
    const { currentBag, bagCount } = this.data;

    if (currentBag >= bagCount) {
      this.setData({ phase: 'done', progress: 100, displayTime: '全部完成 🎉' });
      app.globalData.infusionState = null;
      wx.showModal({
        title:      '🎉 输液完成',
        content:    '所有输液已完成！请通知护士拔针。',
        showCancel: false,
        confirmText: '好的',
      });
    } else {
      wx.showModal({
        title:       `第 ${currentBag} 袋输完`,
        content:     `请护士更换第 ${currentBag + 1} 袋药液后，点击「已换上」继续计时`,
        confirmText: '已换上，继续',
        cancelText:  '稍等',
        success: r => {
          if (r.confirm) this._nextBag();
          else this.setData({ phase: 'paused', bagElapsed: this.data.minutesPerBag * 60 });
        },
      });
    }
  },

  _nextBag() {
    const next = this.data.currentBag + 1;
    const bags = this.data.bags.map((b, i) => ({
      ...b,
      done:   i + 1 < next,
      active: i + 1 === next,
    }));
    const adjustedStart = Date.now();
    this.setData({ currentBag: next, bags, phase: 'running', adjustedStart, bagElapsed: 0, progress: 0 });
    this._updateDisp(0, this.data.minutesPerBag * 60);
    this._save();
    this._startTick();
    wx.showToast({ title: `开始第 ${next} 袋`, icon: 'none' });
  },

  // ── Config ───────────────────────────────────────────────────────────────
  setBags(e) {
    if (this.data.phase !== 'config') return;
    const n = parseInt(e.currentTarget.dataset.n);
    this.setData({
      bagCount:   n,
      currentBag: 1,
      bags: Array.from({ length: n }, (_, i) => ({ n: i + 1, done: false, active: i === 0 })),
    });
  },

  onMinInput(e) {
    if (this.data.phase !== 'config') return;
    const m  = Math.max(1, parseInt(e.detail.value) || 60);
    const mm = String(m).padStart(2, '0');
    this.setData({ minutesPerBag: m, displayTime: `${mm}:00` });
  },

  // ── Controls ─────────────────────────────────────────────────────────────
  startPause() {
    const { phase, bagElapsed } = this.data;
    if (phase === 'config' || phase === 'paused') {
      const adjustedStart = Date.now() - bagElapsed * 1000;
      this.setData({ phase: 'running', adjustedStart });
      this._save();
      this._startTick();
    } else if (phase === 'running') {
      this._stopTick();
      const el = getElapsed(this.data);
      this.setData({ phase: 'paused', bagElapsed: el });
      this._save();
    }
  },

  reset() {
    wx.showModal({
      title:   '重置输液计时',
      content: '确定要重置计时吗？当前进度将清零。',
      success: r => {
        if (!r.confirm) return;
        this._stopTick();
        app.globalData.infusionState = null;
        const { bagCount, minutesPerBag } = this.data;
        const mm = String(minutesPerBag).padStart(2, '0');
        this.setData({
          phase:         'config',
          currentBag:    1,
          adjustedStart: 0,
          bagElapsed:    0,
          progress:      0,
          bags: Array.from({ length: bagCount }, (_, i) => ({ n: i + 1, done: false, active: i === 0 })),
          displayTime:   `${mm}:00`,
        });
      },
    });
  },
});
