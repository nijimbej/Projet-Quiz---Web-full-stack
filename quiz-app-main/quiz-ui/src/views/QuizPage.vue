<template>
  <div class="about">
    <div style=" margin-top: 2%; margin-bottom: 2%;">
      <form class="form-control" style=" margin-left: 20%;" v-if="showForm" @submit.prevent="onSubmit">
        Player name : <br>
        <input class="form-control" style="size:20px" type="text" id="playerName" v-model="playerName">
        <template v-for="(question, qIndex) in questions">
          <h4 style="color:#056895">{{ question.title }}</h4>
          <b>
            <p>{{ question.text }}</p>
          </b>
          <img style="width:200px; border-radius: 4%;   border: 1px solid #ddd;" :src="question.image" alt="Image" />
          <br><br>
          <template v-for="(answer, aIndex) in question.possibleAnswers">
            <label>
              <input class="form-check-input" type="radio" v-bind:value="answer.text"
                v-bind:name="'question-' + question.id" v-model="question.selectedAnswer"
                @change="selectedAnswerIndexes[qIndex] = aIndex + 1">
              {{ answer.text }}
            </label><br>
          </template>
        </template>
        <br>
        <br>
        <button class="btn btn-danger" type="submit">Envoyer</button>
      </form>
    </div>
    <div style="margin-left:300px" v-if="!showForm" >
      <h2 style="color:#056895">Bonjour  {{ playerName }} Votre score est : {{ numCorrect }}/10 !</h2>
      <h4 style="color:green"> Classement actuel  : </h4> <br>
      <table  class="table table-bordered">
  <thead>
    <tr>
     
      <th scope="col">Player Name </th>
      <th scope="col" style="color:red" >Score</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="scoreEntry in quizInfos.data.scores" v-bind:key="scoreEntry.date">

      <th style="color:#056895" scope="row">{{ scoreEntry.playerName }}</th>
      <td>{{ scoreEntry.score }}</td>
    </tr>
    
  </tbody>
</table>
      <button class="btn btn-primary" @click="goToHome">Home</button>
    </div>
  </div>
</template>

<script>

import quizApiService from "@/services/QuizApiService";
import axios from "axios";

export default {
  data() {
    return {
      showForm: true,
      questions: [],
      selectedAnswerIndexes: [],
      numCorrect: 0,
      playerName: '',
      quizInfos: {},
    }
  },
  created() {
    try {
      quizApiService.getQuestions().then((data) => {
        this.questions = data.data
      })
    } catch (error) {
      console.error(error)
    }
    for (const question of this.questions) {
      question.selectedAnswer = '';
    }
    try {
      quizApiService.getQuizInfo().then((data) => {
        this.quizInfos = data
      });
    } catch (error) {
      console.error(error)
    }
  },
  methods: {
    async onSubmit() {
      this.questions.forEach(question => {
        question.possibleAnswers.forEach(answer => {
          //this.answers.push(answer.indexOf(question.selectedAnswer))
          if (answer.text === question.selectedAnswer) {
            if (answer.isCorrect) { console.log('Correct!'); this.numCorrect++; }
            else { console.log('Incorrect!') }
          }
        })
        this.showForm = false;
      });
      try {
        // Send the POST request to the Flask server
        const response = await axios.post('http://127.0.0.1:5000/participations', {
          playerName: this.playerName,
          answers: this.selectedAnswerIndexes
        });
        console.log(response.data); // Log the response data
      } catch (error) {
        console.error(error); // Log the error
      };
    },
    goToHome() {
      this.$router.push('/');
    },
  }
}
</script>