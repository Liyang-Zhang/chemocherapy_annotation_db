<template>
  <v-container>
    <v-card>
      <v-card-title>
        ChemoGene List
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="openDialog('add')">Add New</v-btn>
        <v-btn color="primary" @click="toggleUploadDialog">Upload Excel</v-btn>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="chemoGenes"
        :search="search"
        class="elevation-1"
        @click:row="openDialog('edit', $event)"
      >
        <template v-slot:top>
          <v-text-field v-model="search" label="Search" class="mx-4"></v-text-field>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small @click="openDialog('edit', item)">mdi-pencil</v-icon>
          <v-icon small @click="deleteGene(item.id)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ dialogMode === 'add' ? 'Add New Gene' : 'Edit Gene' }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editedItem.gene_name" label="Gene Name"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.description" label="Description"></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="saveGene">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="uploadDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Upload Excel File</span>
        </v-card-title>
        <v-card-text>
          <upload-excel @fileUploaded="fetchGenes"/>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="toggleUploadDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import UploadExcel from '../components/UploadExcel.vue';

export default {
  name: 'GeneList',
  components: {
    UploadExcel
  },
  data() {
    return {
      chemoGenes: [],
      search: '',
      dialog: false,
      uploadDialog: false,
      dialogMode: '',
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Gene Name', value: 'gene_name' },
        { text: 'Description', value: 'description' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      editedIndex: -1,
      editedItem: {
        id: '',
        gene_name: '',
        description: ''
      },
    };
  },
  created() {
    this.fetchGenes();
    this.printCookies();
  },
  methods: {
    fetchGenes() {
      this.$axios.get('/api/Chemogene/')
        .then(response => {
          this.chemoGenes = response.data;
        })
        .catch(error => {
          console.error('There was an error!', error);
        });
    },
    openDialog(mode, item = { id: '', gene_name: '', description: '' }) {
      this.dialogMode = mode;
      if (mode === 'edit') {
        this.editedIndex = this.chemoGenes.indexOf(item);
        this.editedItem = { ...item };
      } else {
        this.editedItem = { id: '', gene_name: '', description: '' };
      }
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.editedItem = { id: '', gene_name: '', description: '' };
    },
    toggleUploadDialog() {
      this.uploadDialog = !this.uploadDialog;
    },
    saveGene() {
      const csrfToken = this.$cookies.get('csrftoken');
      if (this.dialogMode === 'edit') {
        this.$axios.put(`/api/Chemogene/${this.editedItem.id}/`, this.editedItem, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          }
        })
          .then(() => {
            Object.assign(this.chemoGenes[this.editedIndex], this.editedItem);
            this.closeDialog();
          })
          .catch(error => {
            console.error(error);
          });
      } else {
        this.$axios.post('/api/Chemogene/', this.editedItem, {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          }
        })
          .then(response => {
            this.chemoGenes.push(response.data);
            this.closeDialog();
          })
          .catch(error => {
            console.error(error);
          });
      }
    },
    deleteGene(id) {
      const csrfToken = this.$cookies.get('csrftoken');
      this.$axios.delete(`/api/Chemogene/${id}/`, {
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      .then(() => {
        const index = this.chemoGenes.findIndex(gene => gene.id === id);
        this.chemoGenes.splice(index, 1);
      })
      .catch(error => {
        console.error(error);
      });
    },
    printCookies() {
      const allCookies = this.$cookies.keys();
      console.log('All cookies:', allCookies);
      allCookies.forEach(cookieName => {
        console.log(`${cookieName}:`, this.$cookies.get(cookieName));
      });
    }
  }
}
</script>

<style scoped>
.v-card-title {
  font-weight: bold;
}

.v-btn {
  margin: 0 5px;
}

.v-data-table {
  margin-top: 80px;
}

.v-dialog {
  text-align: left;
}

.v-card-actions {
  justify-content: flex-end;
}
</style>
