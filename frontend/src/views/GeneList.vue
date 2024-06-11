<template>
  <v-container>
    <v-card>
      <v-card-title>
        ChemoGene List
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="openDialog">Add New</v-btn>
        <v-btn color="primary" @click="toggleUploadDialog">Upload Excel</v-btn>
        <v-btn color="primary" @click="downloadExcel">Download Excel</v-btn>
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
                <v-text-field v-model="editedItem.hgnc_id" label="HGNC ID"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedItem.gene_symbol" label="Gene Symbol"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.description_cn" label="Description (CN)"></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.description_en" label="Description (EN)"></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.created_at" label="Created at"></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.updated_at" label="Updated at"></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-select v-model="editedItem.status" :items="statuses" label="Status"></v-select>
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
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';
// import XLSX from 'xlsx';

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
      statuses: ['Active', 'Inactive'],
      headers: [
        { title: 'HGNC ID', align: 'start', key: 'hgnc_id' },
        { title: 'Gene Symbol', align: 'end', key: 'gene_symbol' },
        { title: 'Description (CN)', align: 'end', key: 'description_cn' },
        { title: 'Description (EN)', align: 'end', key: 'description_en' },
        { title: 'Created At', align: 'end', key: 'created_at' },
        { title: 'Updated At', align: 'end', key: 'updated_at' },
        { title: 'Status', align: 'end', key: 'status' },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
      editedIndex: -1,
      editedItem: {
        hgnc_id: '',
        gene_symbol: '',
        description_cn: '',
        description_en: '',
        status: '',
      },
      defaultItem: {
        hgnc_id: '',
        gene_symbol: '',
        description_cn: '',
        description_en: '',
        status: '',
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
      console.log('Deleting item:', this.editedItem.id); // Log the ID for debugging
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
    downloadExcel() {
      try {
        const ws = XLSX.utils.json_to_sheet(this.chemoGenes);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "ChemoGenes");
        const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

        // 生成当前日期和时间作为后缀
        const now = new Date();
        const dateStr = now.toISOString().slice(0, 10); // YYYY-MM-DD
        const timeStr = now.toTimeString().slice(0, 8).replace(/:/g, '-'); // HH-MM-SS

        const fileName = `ChemoGenes_${dateStr}_${timeStr}.xlsx`;

        saveAs(new Blob([wbout], { type: 'application/octet-stream' }), fileName);
      } catch (error) {
        console.error('Error downloading Excel:', error);
      }
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
