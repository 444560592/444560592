// pages/index/index.js — 首页
const app = getApp();

let _refreshTimer = null;

Page({
  data: {
    greeting: '',
    currentDate: '',
    patientName: '',
    pendingTasks: [],
    pendingCount: 0,
    doneCount: 0,
    allDone: false,
    noTasks: true,
    infusionActive: false,
    infusionRemain: '',
    infusionProgress: 0,
  },

  onShow() {
    this._refresh();
    if (_refreshTimer) clearInterval(_refreshTimer);
    _refreshTimer = setInterval(() => this._updateInfusion(), 5000);
  },

  onHide() {
    if (_refreshTimer) { clearInterval(_refreshTimer); _refreshTimer = null; }
  },

  onUnload() {
    if (_refreshTimer) { clearInterval(_refreshTimer); _refreshTimer = null; }
  },

  _refresh() {
    this._greeting();
    this._tasks();
    this._updateInfusion();
  },

  _greeting() {
    const now = new Date();
    const h = now.getHours();
    const greeting = h < 12 ? '上午好' : h < 18 ? '下午好' : '晚上好';
    const m = now.getMonth() + 1;
    const d = now.getDate();
    const wd = ['日', '一', '二', '三', '四', '五', '六'][now.getDay()];
    this.setData({
      greeting,
      currentDate: `${m}月${d}日 星期${wd}`,
      patientName: app.globalData.patientName,
    });
  },

  _tasks() {
    const STATUS_LABELS = { pending: '待办', doing: '进行中', done: '已完成' };
    const all = app.globalData.tasks;
    const pendingAll = all.filter(t => t.status !== 'done');
    const pendingCount = pendingAll.length;
    const doneCount = all.filter(t => t.status === 'done').length;
    const pendingTasks = pendingAll.slice(0, 3).map(t => ({
      ...t,
      statusLabel: STATUS_LABELS[t.status] || '待办',
    }));
    this.setData({
      pendingTasks,
      pendingCount,
      doneCount,
      allDone: all.length > 0 && pendingCount === 0,
      noTasks: all.length === 0,
    });
  },

  _updateInfusion() {
    const s = app.globalData.infusionState;
    if (!s || s.phase === 'config' || s.phase === 'done') {
      this.setData({ infusionActive: false });
      return;
    }
    const bagSec = s.minutesPerBag * 60;
    const elapsed = s.phase === 'running'
      ? Math.floor((Date.now() - s.adjustedStart) / 1000)
      : s.bagElapsed;
    if (elapsed >= bagSec) {
      this.setData({ infusionActive: false });
      return;
    }
    const rem = bagSec - elapsed;
    const mm = Math.floor(rem / 60);
    const ss = rem % 60;
    this.setData({
      infusionActive: true,
      infusionProgress: Math.round(elapsed / bagSec * 100),
      infusionRemain: `${mm}分${String(ss).padStart(2, '0')}秒`,
    });
  },

  goTasks()   { wx.switchTab({ url: '/pages/tasks/tasks' }); },
  goInfusion(){ wx.switchTab({ url: '/pages/infusion/infusion' }); },

  callNurse() {
    wx.showModal({
      title: '叫护士',
      content: '确认呼叫护士前来协助？',
      confirmText: '确认呼叫',
      success: res => {
        if (res.confirm)
          wx.showToast({ title: '护士已被通知 ✓', icon: 'none', duration: 2500 });
      },
    });
  },
});
