<template>
  <div class="templates">
    <h1>
      <i class="fas fa-envelope"></i> Templates
      <i class="fas fa-plus-circle create-icon" @click="createTemplate"></i>
    </h1>
    <error v-if="error" :error="error"/>
    <template-table v-if="templates" :templates="templates" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @accept="deleteTemplate"/>
    <create-template :visible.sync="showCreateModal" @created="getTemplates"/>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";

import TemplateTable from "@/components/TemplateTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import Error from "@/components/Error.vue";

export default {
  name: "Templates",
  components: {
    TemplateTable,
    ConfirmModal,
    CreateTemplate,
    Error
  },
  data: () => ({
    templates: null,
    showDeleteModal: false,
    selectedTemplate: null,
    showCreateModal: false,
    error: null
  }),
  created() {
    this.getTemplates();
  },
  methods: {
    async getTemplates() {
      try {
        let response = await templatesApi.getAll();
        this.templates = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    showModal(template_id) {
      this.showDeleteModal = true;
      this.selectedTemplate = template_id;
    },
    async deleteTemplate() {
      this.showDeleteModal = false;
      try {
        await templatesApi.delete(this.selectedTemplate);
      } catch (error) {
        this.error = error.response;
      }
      this.getTemplates();
    },
    createTemplate() {
      this.showCreateModal = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.templates {
  position: relative;
}
</style>
