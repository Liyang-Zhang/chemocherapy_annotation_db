<template>
  <v-container>
    <v-card>
      <v-card-title>
        ChemoGene List
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="openDialog">Add New</v-btn>
        <v-btn color="primary" @click="toggleUploadDialog">Upload Excel</v-btn>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="chemoGenes"
        :search="search"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-text-field v-model="search" label="Search" class="mx-4"></v-text-field>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small @click="editItem(item)">mdi-pencil</v-icon>
          <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
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

    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
          <v-spacer></v-spacer>
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
      dialogDelete: false,
      dialogMode: '',
      headers: [
        { title: 'ID', align: 'start', key: 'id' },
        { title: 'Gene Symbol', align: 'end', key: 'gene_name' },
        { title: 'Description', align: 'end', key: 'description' },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      editedIndex: -1,
      editedItem: {
        id: '',
        gene_name: '',
        description: ''
      },
      defaultItem: {
        id: '',
        gene_name: '',
        description: ''
      },
    };
  },
  created() {
    this.fetchGenes();
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
    openDialog() {
      this.dialogMode = 'add';
      this.dialog = true;
    },
    editItem(item) {
      this.dialogMode = 'edit';
      this.editedIndex = this.chemoGenes.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.chemoGenes.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    closeDialog() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
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
    deleteItemConfirm() {
      const csrfToken = this.$cookies.get('csrftoken');
      this.$axios.delete(`/api/Chemogene/${this.editedItem.id}/`, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        }
      })
        .then(() => {
          this.chemoGenes.splice(this.editedIndex, 1);
          this.closeDelete();
        })
        .catch(error => {
          console.error(error);
        });
    },
    toggleUploadDialog() {
      this.uploadDialog = !this.uploadDialog;
    },
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
