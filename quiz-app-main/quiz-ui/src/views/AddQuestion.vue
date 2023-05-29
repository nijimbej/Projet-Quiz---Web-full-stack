<template >
  <nav style="margin:auto">
    <div>
      <div>
        <label for="title">
          <h5>Title</h5>
        </label>
        <input size="50" class="form-control" type="text" v-model="title" id="title" name="title" placeholder="title">

        <label for="position">
          <h5>Position</h5>
        </label>
        <input class="form-control" type="text" v-model="position" id="position" name="position" placeholder="position">

        <label for=" text">
          <h5>Text</h5>
        </label>
        <input class="form-control" type="text" v-model="text" id="text" name="text" placeholder="text">

        <label for="image">
          <h5>Image</h5>
        </label>
        <input class="form-control" type="text" v-model="image" id="image" name="image" placeholder="image">

        <label for="answers">
          <h5>Answers</h5>
        </label>
        <div class="table4">
          <div v-for="(answer, index) in answers">
            <div v-if="index + 1 == selected" class="correctAnswers">
              <label for="answer"> Answer: {{ index + 1 }}</label>
              <input id="answer" class="form-control" type="text" v-model="answer.text" placeholder="text">
            </div>
            <div v-else class="incorrectAnswers">
              <label for="answer"> Answer: {{ index + 1 }}</label>
              &nbsp <button type="button" class="btn btn-info" v-on:click="selectAnswer(index + 1)">Select as correct</button>
              <input class="form-control" id="answer" type="text" v-model="answer.text" placeholder="text">
            </div> 
            <br>
          </div>
          <div class="table">
            <div>
              <input type="submit" class="btn btn-primary" value="add answer" v-on:click="addAnswers">
              &nbsp
              <input class="btn btn-danger" type="submit" value="remove answer" v-on:click="removeAnswers">
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div>
        <input type="submit" class="btn btn-success" value="submit" v-on:click="send">
        <div class="red" v-if="invalidForm">Invalid</div>
      </div>
    </div>
  </nav>

</template>
<script>
import axios from "axios";
export default {
  emits: ['cancel', 'submit'],
  props: {
    sizeQuiz: Number
  },
  data() {
    var title = ""
    var text = ""
    var image = ""
    var answers = []
    var position = 1
    var selected = null
    var invalidForm = false
    var answersSize = 0
    return { text, title, position, image, answers, selected, invalidForm, answersSize }
  },
  created() {
    console.log("creation question")
    this.addAnswers()
    this.selected = 1
  },
  methods: {
    selectAnswer(index) {
      this.selected = index
    },
    addAnswers() {
      if (this.answersSize < 4) {
        this.answers.push({ text: "", isCorrect: false })
        this.answersSize = this.answers.length
      }
    },
    removeAnswers() {
      if (this.answersSize > 1) {
        this.answers.pop()
        this.answersSize = this.answers.length
        if (this.answersSize == this.selected - 1) {
          this.selected--
        }
      }
    },
    validForm() {
      this.invalidForm = false;
      if (this.title == "" | this.text == "") {
        this.invalidForm = true;
      }
      for (var i = 0; i < this.answers.length; i++) {
        if (this.answers[i].text == "") {
          this.invalidForm = true;
        }
        if (i == this.selected - 1) {
          this.answers[i].isCorrect = true;
        }
        else {
          this.answers[i].isCorrect = false;
        }
      }
    },
    async send() {
      this.validForm()
      if (this.invalidForm) {
        return
      }

      // Send the POST request to the Flask server
      const response = await axios.post('http://127.0.0.1:5000/questions', {
        position: Number(this.position),
        title: String(this.title),
        text: String(this.text),
        image: String(this.image),
        possibleAnswers: this.answers
      }, {headers: {Authorization: 'Bearer ' + localStorage.token}});
      console.log(response.data);
      this.$router.push('/admin');
    }
  }
}
</script>