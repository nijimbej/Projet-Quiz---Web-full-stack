import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuizPage from '../views/QuizPage.vue'
import AdminPage from '../views/AdminPage.vue'
import QuestionPage from '../views/QuestionPage.vue'
import AddQuestion from '../views/AddQuestion.vue'
import EditQuestion from '../views/EditQuestion.vue'
import Login from '../views/Login.vue'
import auth from '../middleware/auth'

function checkIfLogged() {
  //const authStore = useAuthStore();
  if (!localStorage.getItem('token')) return '/login';
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/quiz-page',
      name: 'QuizPage',
      component: QuizPage
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: AdminPage,
      beforeEnter: [checkIfLogged], 
      
    },
    {
      path: '/questions/:id',
      name: 'QuestionPage',
      component: QuestionPage,
      props : true,
      beforeEnter: [checkIfLogged], 
    },
    {
      path: '/addQuestion',
      name: 'addQuestion',
      component: AddQuestion,
      beforeEnter: [checkIfLogged], 
    },
    {
      path: '/editQuestion/:id',
      name: 'editQuestion',
      component: EditQuestion,
      beforeEnter: [checkIfLogged], 
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
  ]
})

export default router
