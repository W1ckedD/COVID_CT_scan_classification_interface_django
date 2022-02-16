const logSearchContainer = document.querySelector('#logSearch');
const btnLogSearch = document.querySelector('#btnLogSearch');

btnLogSearch.addEventListener('click', function () {
  logSearchContainer.classList.toggle('show');
});

new Vue({
  el: '#logSearch-vue',
  delimiters: ['[[', ']]'],
  data() {
    return {
      log_username: '',
      log_start_date: '',
      log_end_date: '',
      success: false,
      failure: false,
      AUTH: false,
      READ: false,
      CREATE: false,
      UPDATE: false,
      DELETE: false,
      PREDICT: false,
    };
  },
  created() {
    this.prepopulate();
  },
  methods: {
    prepopulate() {
      const {
        log_username,
        success,
        failure,
        AUTH,
        READ,
        CREATE,
        UPDATE,
        DELETE,
        PREDICT,
        start_date,
        end_date,
      } = Qs.parse(location.search, {
        ignoreQueryPrefix: true,
      });

      this.log_username = log_username;
      this.success = success === 'on';
      this.failure = failure === 'on';
      this.AUTH = AUTH === 'on';
      this.READ = READ === 'on';
      this.CREATE = CREATE === 'on';
      this.UPDATE = UPDATE === 'on';
      this.DELETE = DELETE === 'on';
      this.PREDICT = PREDICT === 'on';
      this.log_start_date = start_date;
      this.log_end_date = end_date;
    },
  },
});
