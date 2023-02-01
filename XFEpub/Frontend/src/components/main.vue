<script setup>
</script>

<template>
    <div class="border p-5 m-2">
        <h1 class="">XenForo Thread Downloader</h1>


        <form action="" class="container">
          <div class="row">
            <label for="thread_url" class="form-label">Choose a thread to download:</label>
            <input type="url" id="thread_url" name="thread_url" class="form-control" style="font-size: 1.4em;">

            </div>

          <div class="row mt-5">
            <div class="col-2">
              <label class="switch">
                  <input type="checkbox" id="acrophyca">
                  <span class="slider round"></span>
              </label>
            </div>
            <div class="col-4">
              <label for="acrophyca" class="form-check-label ms-3">acrophyca</label>
            </div>
            <div class="col-2">
              <label class="switch">
                  <input type="checkbox" id="sidestory">
                  <span class="slider round"></span>
              </label>
            </div>
            <div class="col-4">
              <label for="sidestory" class="form-check-label ms-3">Sidestory</label>
            </div>
          </div>

          <div class="row mt-3">
            <div class="col-2">
              <label class="switch">
                  <input type="checkbox" id="info">
                  <span class="slider round"></span>
              </label>
            </div>
            <div class="col-4">
              <label for="info" class="form-check-label ms-3">Informational</label>
            </div>
            
            <div class="col-2">
              <label class="switch">
                  <input type="checkbox" id="media">
                  <span class="slider round"></span>
              </label>
            </div>
            <div class="col-4">
              <label for="media" class="form-check-label ms-3"> Media <small class="">NB: Fetched posts will not have embedded images. </small></label>
            </div>
          </div>
            



        </form>


        <small innerText="Tab Icon: Koreller, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons" class="">
        </small>
    </div>
</template>

<script>
// A script that will hide the toggles when there is no URL in thread_url

// A script taht will send off the url packet


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

</style>