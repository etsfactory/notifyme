<template>
  <sorteable-table :columns="columns" :data="templates" class="templates-table">
    <template slot="row" slot-scope="template">
      <td>{{ template.row.id }}</td>
      <td>{{ template.row.name }}</td>
      <td>{{ template.row.subject }}</td>
      <td class="actions">
        <i class="far fa-eye icon" @click="navigateToTemplate(template.row.id)"></i>
        <i class="far fa-trash-alt icon" @click="deleteTemplate(template.row.id)"></i>
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
    }
  },
  data: () => ({
    columns: [
      { text: "Id", key: "id", sorteable: true },
      { text: "name", key: "email", sorteable: true },
      { text: "subject", key: "name", sorteable: true },
      { text: "Actions", key: "actions", sorteable: false }
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
.templates-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-main-dark;
  }
}
</style>
