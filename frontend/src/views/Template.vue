<template>
  <div>
    <Error v-if="error" :error="error" />
    <div v-if="template">
      <TheHeader>
        <template slot="title">
          Template
        </template>
        <template slot="buttons">
          <router-link to="/bus_filters" class="link">
            <i class="fas fa-chevron-left" />Back to templates
          </router-link>
        </template>
      </TheHeader>
      <div class="template">
        <div class="template-container">
          <div class="buttons">
            <action-buttons
              @edit="showEditModal"
              @remove="showDeleteTemplate = true"
            />
            <confirm-modal
              :visible.sync="showDeleteTemplate"
              @accept="deleteTemplate"
              subtitle="This action can not be undone. All bus filters asociated with this template will be replaced with default template"
            />
            <KeyValueTable class="info" :data="template" disable="text" />
          </div>
        </div>
        <div class="right">
          <div class="text">
            <h2>Body of the email:</h2>
            <pre v-highlightjs>
              <code class="html text-body">{{ textHTML }}</code>
            </pre>
          </div>
          <div class="bus_filters">
            <div class="right-title">
              <h2 class="notifications-title">
                Bus filters with this template:
              </h2>
              <button class="button-create" @click="setModalBusFilter">
                <img
                  svg-inline
                  class="create-icon"
                  src="../assets/icons/plus.svg"
                />Add bus filter
              </button>
            </div>
            <bus-filters-table v-if="templateFilters" :bus-filters="templateFilters" disable-delete/>
          </div>
          <div v-if="showModalBusFilter" class="modal" id="modal">
            <div class="modal-bg" @click="setModalBusFilter(false)" />
            <div class="modal-inner">
              <a class="modal-close" @click="setModalBusFilter(false)">X</a>
              <error v-if="error" :error="error" />
              <ul class="list">
                <li
                  v-for="(busFilter, i) in filteredBusFilters"
                  :key="i"
                  class="bus-filter"
                >
                  <div class="info">
                    <div class="name">
                      <span class="id">{{ busFilter.exchange }}</span>
                      {{ busFilter.key }}
                    </div>
                    <div>{{ busFilter.description }}</div>
                  </div>
                  <div class="button">
                    <div class="toggler">
                      <toggler :toggled="isBusFilterSuscribed(busFilter.id)" @click="selectBusFilter(busFilter, $event)"/>
                    </div>
                  </div>
                </li>
              </ul>
              <div class="center">
                <button
                  class="button-main button-submit"
                  @click="addBusFilters"
                >
                  <img
                    svg-inline
                    class="create-icon"
                    src="../assets/icons/plus.svg"
                  />
                  Add bus filters
                </button>
              </div>
            </div>
          </div>
          <create-template
            :model="template"
            :visible.sync="showCreateModal"
            :edit="true"
            @created="$router.go(0)"
            :code="textHTML"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";
import busFiltersApi from "@/logic/bus_filters";
import beautify from "js-beautify";
import KeyValueTable from "@/components/KeyValueTable.vue";
import TheHeader from "@/components/TheHeader.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import Error from "@/components/Error.vue";
import BusFiltersTable from "@/components/BusFiltersTable.vue";
import Toggler from "@/components/Toggler.vue";

export default {
  name: "Template",
  components: {
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    TheHeader,
    CreateTemplate,
    Error,
    BusFiltersTable,
    Toggler
  },
  data: () => ({
    template: null,
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false,
    showDeleteTemplate: false,
    textHTML: "",
    editedText: "",
    error: null,
    templateFilters: null,
    showModalBusFilter: false,
    selectedbusFilters: [],
    busFilters: []
  }),
  created() {
    this.getTemplate();
    this.getTemplateFilters();
    this.getBusFilters();
  },
  computed: {
    filteredBusFilters() {
      return this.busFilters.filter(item => !this.isBusFilterSuscribed(item.id));
    }
  },
  methods: {
    async getTemplate() {
      try {
        let response = await templatesApi.get(this.$route.params.id);
        this.template = response.data;
        let text_breaks = response.data.text
          .replace(/(\r\n\t|\n|\r\t)/gm, "")
          .replace(/{%/g, "\n{%")
          .replace(/%}/g, "%}\n");
        this.textHTML = beautify.html(text_breaks, {
          indent_size: 2,
          wrap_line_length: 100
        });
      } catch (error) {
        this.error = error.response;
      }
    },
    async getBusFilters() {
      try {
        let response = await busFiltersApi.getAll();
        this.busFilters = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    async getTemplateFilters() {
      try {
        let response = await templatesApi.getFilters(this.$route.params.id);
        this.templateFilters = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    async deleteTemplate() {
      try {
        await templatesApi.delete(this.template.id);
        this.$router.push("/templates");
      } catch (error) {
        this.error = error.response;
      }
    },
    async deleteBusFilter(busFilter) {
      this.setModalBusFilter(false);
      try {
        await templatesApi.deleteBusFilter(this.template.id, busFilter);
        this.getTemplate();
        this.getTemplateFilters();
      } catch (error) {
        this.error = error.response;
      }
    },
    async addBusFilters() {
      this.setModalBusFilter(false);
      try {
        await templatesApi.addBusFilters(this.template.id, this.selectedbusFilters);
        this.getTemplate();
        this.getTemplateFilters();
      } catch (error) {
        console.log(error);
        this.error = error.response;
      }
    },
    selectBusFilter(busFilter, toggled) {
      if (toggled) {
        this.selectedbusFilters.push(busFilter);
      } else {
        let index = this.selectedbusFilters.indexOf(busFilter);
        if (index > -1) {
          this.selectedbusFilters.splice(index, 1);
        }
      }
    },
    isBusFilterSuscribed(id) {
      return this.templateFilters.some(item => item.id === id);
    },
    showEditModal() {
      this.showCreateModal = true;
    },
    showDeleteModal(id) {
      this.showConfirmModal = true;
      this.selectedUser = id;
    },
    closeDeleteModal() {
      this.showConfirmModal = false;
    },
    setModalBusFilter(state) {
      this.showModalBusFilter = state;
    }
  }
};
</script>

<style lang="scss" scoped>
.header {
  width: 24%;
}
.template {
  position: relative;
  display: flex;
}
.notifications-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-secundary;
  }
}
.users {
  margin-top: 3rem;
}
.template-container {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 3rem;
}
.buttons {
  width: 100%;
}
.text-body {
  padding: 1rem 2rem;
}
.button-grey {
  margin-left: 1rem;
}
.button-edit {
  margin-top: -3rem;
}
pre {
  margin: 0;
}
.right {
  width: 75%;
  margin-top: -78px;
}
.link {
  text-decoration: none;
  color: #828282;
}
.fa-chevron-left {
  color: $color-main;
  margin-right: 0.5rem;
}
.right-title {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5rem;
}
.button-create {
  background: transparent;
  border: none !important;
  cursor: pointer;
  color: #333333;
  border-radius: 3px;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  font-size: 0.8rem;
  height: 45px;
  padding: 0 1rem;
  &:hover {
    background: rgba(0, 0, 0, 0.04);
  }
}

.bus-filter-list,
.bus-filter-subscription {
  width: 100%;
  margin: 0;
}
.bus-filter-list {
  overflow-y: auto;
  max-height: 700px;
  padding: 1rem 0;
}
.bus-filter {
  width: 48%;
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  background: #f2f2f2;
  border-radius: 5px;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.info {
  width: 80%;
  padding: 1rem;
}
.button {
  padding: 1rem;
}
.name {
  font-size: 1.2rem;
}
.id {
  font-weight: bold;
  padding-right: 10px;
}
.toggler {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.sub-button {
  margin-top: 3rem;
}
.list {
  display: flex;
  justify-content: space-between;
  padding: 0;
  flex-wrap: wrap;
}
</style>
