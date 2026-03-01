// pages/tasks/tasks.js — 就诊任务管理
const app = getApp();

const TEMPLATES = [
  { name: '挂号',         location: '一楼门诊大厅挂号窗口',          priority: 'high'   },
  { name: '就诊 / 问诊',  location: '儿科门诊（见挂号单楼层）',       priority: 'high'   },
  { name: '缴费',         location: '一楼收费窗口 / 自助缴费机',      priority: 'normal' },
  { name: '抽血化验',     location: '检验科采血室',                   priority: 'normal' },
  { name: '送检标本',     location: '检验科标本接收窗口',             priority: 'normal' },
  { name: '取化验报告',   location: '自助打印机 / 检验科窗口',        priority: 'normal' },
  { name: '取药',         location: '一楼药房取药窗口',               priority: 'normal' },
  { name: '输液 / 注射',  location: '儿科输液室',                    priority: 'normal' },
  { name: '拍片 / CT',    location: '影像科（见申请单楼层）',         priority: 'normal' },
  { name: '超声检查',     location: '超声科',                        priority: 'normal' },
  { name: '心电图',       location: '心电图室',                      priority: 'normal' },
];

const STATUS_LABELS = { pending: '待办', doing: '进行中', done: '已完成' };
const STATUS_NEXT   = { pending: 'doing', doing: 'done', done: 'pending' };

Page({
  data: {
    displayTasks: [],
    activeFilter: 'all',
    totalCount:   0,
    pendingCount: 0,
    doneCount:    0,
    showModal: false,
    showTpl:   false,
    templates: TEMPLATES,
    newName: '',
    newLoc:  '',
    newPri:  'normal',
  },

  onShow() { this._refresh(); },

  _refresh(filter) {
    filter = filter || this.data.activeFilter;
    const all          = app.globalData.tasks;
    const totalCount   = all.length;
    const pendingCount = all.filter(t => t.status !== 'done').length;
    const doneCount    = all.filter(t => t.status === 'done').length;
    let list = all;
    if (filter === 'pending') list = all.filter(t => t.status !== 'done');
    if (filter === 'done')    list = all.filter(t => t.status === 'done');
    const displayTasks = list.map(t => ({ ...t, statusLabel: STATUS_LABELS[t.status] || '待办' }));
    this.setData({ displayTasks, activeFilter: filter, totalCount, pendingCount, doneCount });
  },

  setFilter(e) { this._refresh(e.currentTarget.dataset.filter); },

  toggleStatus(e) {
    const id   = e.currentTarget.dataset.id;
    const task = app.globalData.tasks.find(t => t.id === id);
    if (task) {
      task.status = STATUS_NEXT[task.status] || 'pending';
      app.saveTasks();
      this._refresh();
    }
  },

  deleteTask(e) {
    const id = e.currentTarget.dataset.id;
    wx.showModal({
      title:   '删除任务',
      content: '确定要删除这个任务吗？',
      success: r => {
        if (r.confirm) {
          app.globalData.tasks = app.globalData.tasks.filter(t => t.id !== id);
          app.saveTasks();
          this._refresh();
        }
      },
    });
  },

  openModal() {
    this.setData({ showModal: true, showTpl: false, newName: '', newLoc: '', newPri: 'normal' });
  },

  closeModal() { this.setData({ showModal: false }); },
  toggleTpl()  { this.setData({ showTpl: !this.data.showTpl }); },

  useTpl(e) {
    const t = TEMPLATES[e.currentTarget.dataset.idx];
    this.setData({ newName: t.name, newLoc: t.location, newPri: t.priority, showTpl: false });
  },

  onNameIn(e) { this.setData({ newName: e.detail.value }); },
  onLocIn(e)  { this.setData({ newLoc:  e.detail.value }); },
  setPri(e)   { this.setData({ newPri:  e.currentTarget.dataset.p }); },

  confirmAdd() {
    const name = this.data.newName.trim();
    if (!name) {
      wx.showToast({ title: '请输入任务名称', icon: 'none' });
      return;
    }
    app.globalData.tasks.push({
      id:       Date.now().toString(),
      name,
      location: this.data.newLoc.trim() || '未指定地点',
      priority: this.data.newPri,
      status:   'pending',
    });
    app.saveTasks();
    this.setData({ showModal: false });
    this._refresh();
    wx.showToast({ title: '已添加 ✓', icon: 'none' });
  },

  clearDone() {
    wx.showModal({
      title:   '清除已完成',
      content: '确认清除所有已完成的任务？',
      success: r => {
        if (r.confirm) {
          app.globalData.tasks = app.globalData.tasks.filter(t => t.status !== 'done');
          app.saveTasks();
          this._refresh();
        }
      },
    });
  },
});
