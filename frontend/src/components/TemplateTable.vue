<template>
  <sorteable-table :columns="columns" :data="templates" class="templates-table">
    <template slot="row" slot-scope="template">
      <td>{{ template.row.id }}</td>
      <td>{{ template.row.name }}</td>
      <td>{{ template.row.subject }}</td>
      <td class="actions">
        <img svg-inline class="icon" src="../assets/icons/eye.svg" @click="navigateToTemplate(template.row.id)">
        <img v-if="remove && template.row.name !== 'default'" svg-inline class="icon trash" src="../assets/icons/trash.svg" @click="deleteTemplate(template.row.id)">
      </td>
    </template>
  </sorteable-table>
</template>

<script>
import SorteableTable from "@/components/SorteableTable.vue";

export default {
  name: "TemplateTable",
  components: {
    SorteableTable
  },
  props: {
    templates: {
      type: Array,
      required: true
    },
    remove: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    columns: [
      { text: "ID", key: "id", sorteable: true },
      { text: "Name", key: "email", sorteable: true },
      { text: "Subject", key: "name", sorteable: true },
      { text: "", key: "actions", sorteable: false }
    ]
  }),
  methods: {
    navigateToTemplate(template_id) {
      this.$router.push({ name: "template", params: { id: template_id } });
    },
    deleteTemplate(template_id) {
      this.$emit("deleted", template_id);
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
