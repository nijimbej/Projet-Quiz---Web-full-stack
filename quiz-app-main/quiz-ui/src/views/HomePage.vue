
<template>
  

  <div style="margin:auto">
    <img class="c" style="	height:300px; width: 700px; border-radius: 3%;    margin-bottom: 20px;   margin-top: 20px; " src="https://i.ibb.co/ydjc8mr/quiz.png" alt="Card image cap">
    
    <div class="card" >
  <div class="card-body">
    <h5 class="card-title" style="color:#056895">  Bienvenue sur Quiz</h5>
    <p class="card-text">Pour chaque question, une seule réponse est correcte. Une bonne réponse rapporte 1 point. <br> Une mauvaise réponse ne fait pas perdre de points</p>
    <router-link class="btn btn-primary" to="/quiz-page">Participer au quiz</router-link>
  </div>
</div>

    <table class="table table-bordered">
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

    
    <div>

      <p>Nombre de question: {{ quizInfos.data.size }}</p>
    </div>
    <div>
    </div>
  </div>
</template>


<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      quizInfos: {},
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    try {
      quizApiService.getQuizInfo().then((data) => {
        this.quizInfos = data
      });
    } catch (error) {
      console.error(error)
    }
  }
};
</script>