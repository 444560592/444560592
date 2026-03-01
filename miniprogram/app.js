// app.js — 医院助手 全局逻辑
App({
  globalData: {
    tasks: [],
    patientName: '',
    infusionState: null,
  },

  onLaunch() {
    this.globalData.tasks = wx.getStorageSync('hs_tasks') || [];
    this.globalData.patientName = wx.getStorageSync('hs_name') || '';
  },

  saveTasks() {
    wx.setStorageSync('hs_tasks', this.globalData.tasks);
  },

  savePatientName(name) {
    this.globalData.patientName = name;
    wx.setStorageSync('hs_name', name);
  },
});
