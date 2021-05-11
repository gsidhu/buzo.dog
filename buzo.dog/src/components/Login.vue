<template>
  <div class="text-center space-out bg-color"> 
    <form class="form-signin">
      <h4 class="my-3 font-weight-normal">Login with Email</h4>

      <div class="my-2">
        <label for="inputEmail" class="sr-only">Email address</label>
        <input type="email" id="inputEmail" v-model="email" class="form-control" placeholder="Email address" required="" autofocus="" style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAASCAYAAABSO15qAAAAAXNSR0IArs4c6QAAAPhJREFUOBHlU70KgzAQPlMhEvoQTg6OPoOjT+JWOnRqkUKHgqWP4OQbOPokTk6OTkVULNSLVc62oJmbIdzd95NcuGjX2/3YVI/Ts+t0WLE2ut5xsQ0O+90F6UxFjAI8qNcEGONia08e6MNONYwCS7EQAizLmtGUDEzTBNd1fxsYhjEBnHPQNG3KKTYV34F8ec/zwHEciOMYyrIE3/ehKAqIoggo9inGXKmFXwbyBkmSQJqmUNe15IRhCG3byphitm1/eUzDM4qR0TTNjEixGdAnSi3keS5vSk2UDKqqgizLqB4YzvassiKhGtZ/jDMtLOnHz7TE+yf8BaDZXA509yeBAAAAAElFTkSuQmCC&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;" autocomplete="off">
      </div>
      <div class="my-2">
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" v-model="password" class="form-control" placeholder="Password" required="" style="background-image: url(&quot;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAASCAYAAABSO15qAAAAAXNSR0IArs4c6QAAAPhJREFUOBHlU70KgzAQPlMhEvoQTg6OPoOjT+JWOnRqkUKHgqWP4OQbOPokTk6OTkVULNSLVc62oJmbIdzd95NcuGjX2/3YVI/Ts+t0WLE2ut5xsQ0O+90F6UxFjAI8qNcEGONia08e6MNONYwCS7EQAizLmtGUDEzTBNd1fxsYhjEBnHPQNG3KKTYV34F8ec/zwHEciOMYyrIE3/ehKAqIoggo9inGXKmFXwbyBkmSQJqmUNe15IRhCG3byphitm1/eUzDM4qR0TTNjEixGdAnSi3keS5vSk2UDKqqgizLqB4YzvassiKhGtZ/jDMtLOnHz7TE+yf8BaDZXA509yeBAAAAAElFTkSuQmCC&quot;); background-repeat: no-repeat; background-attachment: scroll; background-size: 16px 18px; background-position: 98% 50%; cursor: auto;" autocomplete="off">
      </div>
      <div class="checkbox mb-3">
        <label>
          <input type="checkbox" value="remember-me"> Remember me
        </label>
      </div>
      <button class="btn btn-lg btn-primary btn-block mb-5" type="submit">Sign in</button>
    </form>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data: function() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    // login: function(e) {
    //   firebase
    //     .auth()
    //     .signInWithEmailAndPassword(this.email, this.password)
    //     .then(
    //       user => {
    //         // alert(`You are logged in as ${user.user.email}`);
    //         user
    //         this.$router.push('/')
    //         // this.$router.go({ path: this.$router.path });
    //       },
    //       err => {
    //         alert(err.message);
    //       }
    //     );
    //   e.preventDefault();
    // }
  }
};
</script>

<style scoped>
.form-signin {
	width: 100%;
	max-width: 330px;
	padding: 15px;
	margin: auto;
}
.space-out {
  margin-top: 5rem !important;
  margin-bottom: 5rem !important;
}
@media screen and (max-width: 768px) {
  .space-out {
  margin-top: 3rem !important;
  margin-bottom: 3rem !important;
}
}
.bg-color {
  /* background: #FFEACB; */
  background-color: #fef7f2;
	overflow: hidden;
	width: 100%;
	border-radius: 16px;
	box-sizing: border-box;
}
.social-signin {
  padding: .5rem;
  border-radius: .3rem; /* matches with Bootstrap default */
  cursor: pointer;
  font-size: 1.25rem;
  color: white;
}
#google-signin {
  background-color: #ea4335;
}
#facebook-signin {
  background-color: #3b5998;
}
a {
  text-decoration: none;
}
</style>