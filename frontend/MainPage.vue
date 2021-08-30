<template>
  <div id="app">
    <v-app id="inspire">
      <v-form>
        <v-file-input v-model="file" color="deep-purple accent-4" counter label="File input" placeholder="Select your files" prepend-icon="mdi-file-upload" outlined :show-size="1000">
        </v-file-input>
        <v-btn @click="submitFile(file)" :disabled="disableSubmit">
          Submit file
        </v-btn>
      </v-form>
      <v-btn @click="triggerUpdate">Refresh</v-btn>
      <v-list-item>
        <v-list-item-group>
          <v-list-item v-for="uf in uploadedFiles" :key="filename">
            <v-card width="900" @click="setSelectedFile(uf.filekey)">
              <v-card-title>{{uf.filename}}</v-card-title>
            </v-card>
          </v-list-item>
        </v-list-item-group>
        </v-list>
        <v-card v-if="selectedFile !== null">
          <v-card-title>Task</v-card-title>
          <v-card-subtitle>{{selectedFile.filename}}</v-card-subtitle>
          <v-card-actions>
            <v-chip-group column multiple active-class="primary" v-model="taskSelectedColumns">
              <v-chip v-for="col in selectedFile.columns" :key="col.colkey" v-if="col.dtype=='object'">{{col.colname}}</v-chip>
            </v-chip-group>
          </v-card-actions>
        </v-card>


    </v-app>
  </div>
</template>

<script>
const BASE_URL = `http://127.0.0.1:8000`;

let vm = new Vue({
  el: "#app",
  vuetify: new Vuetify(),
  data: () => ({
    file: null,
    disableSubmit: true,
    uploadedFiles: null,
    chipSelection: [],
    selectedFile: null,
    taskSelectedColumns: null
  }),
  methods: {
    submitFile(file) {
      console.log("uploading " + file.name);
      let formData = new FormData();
      formData.append("file", this.file);
      axios.post(`http://127.0.0.1:8000/uploadfile/`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
    },
    async fetchUploadedFiles() {
      axios.get(BASE_URL + "/listuploadedfiles/").then(this.setUploadedFiles, this.errUploadedFiles);
    },
    setUploadedFiles (response) {
      console.log("listing files...")
      this.uploadedFiles = response.data.files;
    },
    errUploadedFiles (err) {
      console.log(err);
    },
    triggerUpdate() {
      this.fetchUploadedFiles();
    },
    isRightFile(idx) {
      let selectfilter = function(uf) {
        return uf.filekey === idx;
      }
      return selectfilter
    },
    setSelectedFile(idx) {
      let selectfilter = this.isRightFile(idx);
      if (this.uploadedFiles !== null){
        this.selectedFile = this.uploadedFiles.find(selectfilter);
      }
    },
  },
  beforeUpdate () {
    this.disableSubmit = (this.file === null);
  }
});
</script>
