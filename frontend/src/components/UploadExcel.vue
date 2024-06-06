<template>
  <v-card>
    <v-card-title>Upload Excel File</v-card-title>
    <v-card-text>
      <input type="file" @change="handleFileUpload" />
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="submitFile">Upload</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      file: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submitFile() {
      if (!this.file) return;

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        await fetch('/api/upload_excel/', {
          method: 'POST',
          body: formData,
        });
        this.$emit('fileUploaded');
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Add some styling here if necessary */
</style>
