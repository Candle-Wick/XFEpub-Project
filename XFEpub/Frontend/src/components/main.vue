<script setup>
</script>

<template>
    <div class="border-rounded p-5 m-2">
        <h1 class="">XenForo Thread Downloader</h1>


        <form action="" class="container" v-on:submit.prevent="detectURL">
          <div class="row">
            <label for="thread_url" class="form-label">Choose a thread to download:</label>
            <input type="url" id="thread_url" name="thread_url" class="form-control" style="font-size: 1.4em;" v-model="url" @keyup.enter="">
            <small class="hidden mt-2 text-danger" id="url_error">{{ this.url_error_msg }}</small>

          </div>
          <div class="hidden" id="options">
            <div class="row mt-5">
              <p class="text-start col-7">Select the threadmark catagories that you want in the EPUB file.</p>
            </div>
            <div class="row mt-2">
              <div class="col-2">
                <label class="switch">
                    <input type="checkbox" id="apocrypha"   v-model="apocrypha">
                    <span class="slider round"></span>
                </label>
              </div>
              <div class="col-4 text-start">
                <label for="apocrypha" class="form-check-label ms-3">apocrypha</label>
              </div>
              <div class="col-2">
                <label class="switch">
                    <input type="checkbox" id="sidestory"  v-model="sidestory">
                    <span class="slider round"></span>
                </label>
              </div>
              <div class="col-4 text-start">
                <label for="sidestory" class="form-check-label ms-3">Sidestory</label>
              </div>
            </div>

            <div class="row mt-3">
              <div class="col-2">
                <label class="switch">
                    <input type="checkbox" id="info"  v-model="info">
                    <span class="slider round"></span>
                </label>
              </div>
              <div class="col-4 text-start">
                <label for="info" class="form-check-label ms-3">Informational</label>
              </div>
              
              <div class="col-2">
                <label class="switch">
                    <input type="checkbox" id="media"  v-model="media">
                    <span class="slider round"></span>
                </label>
              </div>
              <div class="col-4 text-start">
                <label for="media" class="form-check-label ms-3"> Media <small class="">NB: Fetched posts will not have embedded images. </small></label>
              </div>
            </div>

            <div class="row d-flex align-items-center justify-content-center mt-3">
              <input type="button" class="col-2 btn btn-info" value="Request EPUB" @click="try_submit">
            </div>
          </div>

        </form>

        <div class="hidden" id= "Result">
          <div id = "loading" class="d-flex justify-content-center align-items-center mt-2"> 
            <p class="text-center m-0 me-2">
              Constructing EPUB file...
            </p>
            <div class="loader align-middle"></div>
          </div>


        </div>
                     
        <div class="mt-5 d-flex justify-content-center">
            <div class="text-start">
            <h1>About</h1>
            <br/>
            <p >This is a student project focused around giving an user the ability to download a fiction hosted on a XenForo based site. <br/>
              To use, enter an valid URL into the textbox. A valid URL is a url that belongs to Spacebattles.com or SufficientVelocity.com, that points towards the thread of a story. <br/>
              Example URLs:
              <ul class="list-group">
                <li class="list-group-item">https://forums.spacebattles.com/threads/the-great-caretaker-of-gaia-overlord-si-player.1069790/</li>
                <li class="list-group-item">https://forums.sufficientvelocity.com/threads/hybrid-hive-eat-shard-worm-mgln.55056/</li>
                <li class="list-group-item">https://forums.sufficientvelocity.com/threads/reverse-engineering-is-not-that-easy-planetary-annihilation-multicross-si.108388/</li>
              </ul>

              <!-- Something about choosing wich parts to grab. -->
            </p>
            </div>
          </div>

        <small innerText="Tab Icon: Koreller, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons" class="">
        </small>
    </div>
</template>

<script>
// A script that will hide the toggles when there is no URL in thread_url

// A script taht will send off the url packet

export default {
  data(){
    return {
      url: "",
      url_error_msg:"",
      apocrypha:false,
      sidestory:false,
      info:false,
      media:false,
    }
  },
  methods: {
    async detectURL(){
      
      if (this.try_url()){
        document.getElementById("options").classList.remove("hidden")
      }
    },
    async try_submit(){

      if (this.try_url()){
        document.getElementById("Result").classList.remove("hidden")
        let body = JSON.stringify({base_url: this.url, apoc: this.apocrypha, sidestory: this.sidestory, info: this.info, media: this.media})
        let requesty = {
                method: "POST",
                headers: {
                    "X-CSRFToken": "",
                    "Content-Type": "application/epub+zip",
                    "Accept": "application/epub+zip"
                },
                body: body
              }

        
        let response = await fetch("http://localhost:8000/api/webscrape_call/", requesty)
        let data = await response
        if (data){
          //Hide loader once message is recived.
          document.getElementById("loading").classList.add("hidden")
        }
        console.log(data)
        // window.location.href = "http";
      }
    },
    try_url(){
      let regex = new RegExp('\/threads\/[a-zA-Z0-9-.]+\/?')


      if ( ["forums.spacebattles.com", "forums.sufficientvelocity.com"].indexOf(new URL(this.url).hostname) == -1)
      {
        this.url_error_msg = "URL is not from an accepted site."
        document.getElementById("url_error").classList.remove("hidden")
        return false
      }

      if ( ! (regex.test(this.url))){
        this.url_error_msg = "An invalid thread detected."
        document.getElementById("url_error").classList.remove("hidden")
        return false
      }
      else {
        document.getElementById("url_error").classList.add("hidden")
      }
      return true
    }

  }
}


</script>

<style>
.hidden {
    display: none;
}
/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #43b15a;
}

input:focus + .slider {
  box-shadow: 0 0 1px #43b15a;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

/* w3 Loader*/
.loader {
  border: 7px solid #f3f3f3; /* Light grey */
  border-top: 7px solid #000000; /* Blue */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  max-width: 40px;
  max-height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>