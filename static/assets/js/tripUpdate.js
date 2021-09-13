new Vue({
    el: "#trip",
    data() {
      return {
        freight: 0.0,
        rate: 0.0,
        weight: 0.0,
        remaining_payment: 0.0,
        expenses: [
          {
            mode: "",
            value: 0.0,
            comment: "",
          },
        ],
        total_expenses: 0.0,
        trucker_name: "",
        trucker_address: "",
        trucker_phone: "",
        trucker_gstin: "",
      };
    },
    mounted() {
        const url_string = window.location.pathname;
        const id = url_string.split('/').pop();
        base_url = window.location.origin;
        url =
          base_url + "/trip/details?id=" + id
        axios
            .get(url)
            .then(response => {
                if (response.status === 200) {
                    data = response.data
                    this.trucker_name = data.trucker_name
                    this.get_trucker()
                    this.expenses = data.expenses
                    this.fill_details(JSON.parse(data.data)[0].fields)
                  }
                })
                .catch((error) => {
                  console.log(error);
            });
    },
    methods: {
      fill_details(data) {
        this.rate =  data.rate
        this.weight = data.weight
        this.freight = data.freight
        this.calculate_freight();
      },
      addExpenseRow() {
        item = { mode: "", value: 0.0 };
        this.expenses.push(item);
      },
      removeExpenseRow(index) {
        this.expenses.splice(index, 1);
        this.calculate_freight();
      },
      calculate_expenses() {
        const l = this.expenses.length;
        total = 0;
        for (let i = 0; i < l; i++) {
          total = total + parseFloat(this.expenses[i].value);
        }
        this.total_expenses = parseFloat(total);
        this.total_expenses = this.round_of(this.total_expenses);
      },
      calculate_freight() {
        this.calculate_expenses();
        this.freight = parseFloat(this.rate) * parseFloat(this.weight);
        this.freight = this.round_of(this.freight);
        let freight = parseFloat(this.freight);
        let expenses = parseFloat(this.total_expenses);
        let remaining = freight - expenses;
        this.remaining_payment = remaining;
        this.remaining_payment = this.round_of(this.remaining_payment);
      },
      get_url(name, party_type) {
        base_url = window.location.origin;
        url =
          base_url +
          "/finance/party?name=" +
          name +
          "&party_type=" +
          party_type;
        return url;
      },
      get_trucker() {
        url = this.get_url(this.trucker_name, "TRUCKER");
        axios
          .get(url)
          .then((response) => {
            if (response.status == 200) {
              data = response.data;

              this.trucker_gstin = data.result.gstin;
              this.trucker_address = data.result.address;
              this.trucker_phone = data.result.phone;
            }
          })
          .catch((error) => {
            console.log(error);
          });
      },
      round_of(val) {
        return Number((val).toFixed(2))
      }
    },
  });
