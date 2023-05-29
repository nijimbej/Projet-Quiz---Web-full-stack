<template>
  <div style="margin:50px">
    <div>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Question</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="question in questions" :key="question.id">
            <td>{{ question.id }}</td>
            <td><router-link :to="{ name: 'QuestionPage', params: { id: question.id } }">{{ question.text }}</router-link></td>          
            <td><router-link class="btn btn-success" :to="{ name: 'editQuestion', params: { id: question.id } }">Éditer</router-link></td>
            <td><button class="btn btn-danger" @click="deleteQuestion(question.id)">Supprimer</button></td>
          </tr>
        </tbody>
      </table>
      <router-link class="btn btn-success" to="/addQuestion">Ajouter une question</router-link>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ref, reactive } from 'vue'
import quizApiService from "@/services/QuizApiService";
import axios from "axios";

export default {
  name: 'Admin',
  setup() {
    const router = useRouter()
    const questions = reactive([])
    const loading = ref(true)
    async function fetchQuestions() {
      try {
        // set loading to true while the data is being fetched
        loading.value = true
        // fetch the questions from the API
        const response = await quizApiService.getQuestions()
        // extract the data from the response object
        const data = response.data
        // update the questions array with the data from the API
        questions.splice(0, questions.length, ...data)
      } catch (error) {
        console.error(error)
      } finally {
        // set loading to false once the data has been fetched
        loading.value = false
      }
    }

    // call fetchQuestions when the component is created
    fetchQuestions()

    function showQuestion(id) {
      // show the question with the specified ID
      router.push(`/questions/${id}`)
    }

    async function deleteQuestion(id) {
      // delete the question with the specified ID
      try {
        const response = await axios.delete(`http://127.0.0.1:5000/questions/${id}`,
        {headers: {Authorization: 'Bearer ' + localStorage.token}});
        location.reload()
      } catch (error) {
        console.error(error)
      }
    }

    return {
      questions,
      loading,
      fetchQuestions,
      deleteQuestion,
      showQuestion
    }
  }
}
</script>
