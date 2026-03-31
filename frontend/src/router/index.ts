import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('@/views/HomeView.vue') },
      { path: 'bli-med', name: 'join', component: () => import('@/views/JoinView.vue') },
      { path: 'terminliste', name: 'schedule', component: () => import('@/views/ScheduleView.vue') },
      { path: 'resultater', name: 'results', component: () => import('@/views/ResultsView.vue') },
      { path: 'lokaler', name: 'rental', component: () => import('@/views/RentalView.vue') },
      { path: 'om-oss', name: 'about', component: () => import('@/views/AboutView.vue') },
      { path: 'kontakt', name: 'contact', component: () => import('@/views/ContactView.vue') },
      { path: 'festival', name: 'festival', component: () => import('@/views/FestivalView.vue') },
      { path: 'nyheter', name: 'news', component: () => import('@/views/NewsView.vue') },
      { path: 'nyheter/:slug', name: 'news-detail', component: () => import('@/views/NewsDetailView.vue') },
      { path: 'oppgave', name: 'puzzle', component: () => import('@/views/PuzzleView.vue') },
      { path: 'logg-inn', name: 'login', component: () => import('@/views/LoginView.vue') },
      { path: 'auth/verify', name: 'auth-verify', component: () => import('@/views/LoginView.vue') },
    ],
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('@/views/admin/DashboardView.vue') },
      { path: 'posts', name: 'admin-posts', component: () => import('@/views/admin/PostsListView.vue') },
      { path: 'posts/:id', name: 'admin-post-edit', component: () => import('@/views/admin/PostEditView.vue') },
      { path: 'events', name: 'admin-events', component: () => import('@/views/admin/EventsListView.vue') },
      { path: 'events/:id', name: 'admin-event-edit', component: () => import('@/views/admin/EventEditView.vue') },
      { path: 'sponsors', name: 'admin-sponsors', component: () => import('@/views/admin/SponsorsListView.vue') },
      { path: 'media', name: 'admin-media', component: () => import('@/views/admin/MediaView.vue') },
    ],
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})
