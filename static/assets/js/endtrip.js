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
        trucker_gstin: "",
        diesel: 0,
      };
    },
    methods: {
      addExpenseRow() {
        item = { mode: "", value: 0.0, comment:"" };
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
        this.total_expenses = parseFloat(total) + parseFloat(this.diesel);
        this.total_expenses = this.round_of(this.total_expenses);
      },
      calculate_freight() {
        this.calculate_expenses();
        this.freight = parseFloat(this.rate) * parseFloat(this.weight);
        this.freight = this.round_of(this.freight);
        this.remaining_payment = parseFloat(this.freight) - this.total_expenses;
        this.remaining_payment = this.round_of(this.remaining_payment);
      },
      get_url(gstin, party_type) {
        base_url = window.location.origin;
        url =
          base_url +
          "/finance/party?gstin=" +
          gstin +
          "&party_type=" +
          party_type;
        return url;
      },
      get_trucker() {
        url = this.get_url(this.trucker_gstin, "TRUCKER");
        axios
          .get(url)
          .then((response) => {
            if (response.status == 200) {
              data = response.data;
              this.trucker_name = data.result.name;
              this.trucker_address = data.result.address;
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
  