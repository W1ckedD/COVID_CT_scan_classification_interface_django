const searchContainer = document.querySelector('#search');
const btnSearch = document.querySelector('#btnSearch');

btnSearch.addEventListener('click', function () {
  searchContainer.classList.toggle('show');
});

new Vue({
  delimiters: ["[[", "]]"],
  el: '#search-vue',
  data() {
    return {
      show: true,
      name: '',
      username: '',
      owner_name: '',
      pos: false,
      neg: false,
      tbd: false,
    };
  },
  created() {
    this.prepopulate();
  },
  methods: {
    prepopulate() {
      const { name, username, owner_name, pos, neg, tbd } = Qs.parse(
        location.search,
        {
          ignoreQueryPrefix: true,
        }
      );
      this.name = name;
      this.username = username;
      this.owner_name = owner_name;
      this.pos = pos === 'on';
      this.neg = neg === 'on';
      this.tbd = tbd === 'on';
    },
  }
});
