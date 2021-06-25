new Vue({
  el: "#consignment",
  data() {
    return {
      rate: 0.0,
      weight: 0.0,
      freight: 0.0,
      remaining_payment: 0.0,
      advance: 0.0,
      consignor_gstin: "",
      consignor_name: "",
      consignor_address: "",
      consignee_gstin: "",
      consignee_name: "",
      consignee_address: "",
    };
  },
  methods: {
    calculate_freight() {
      this.freight = this.rate * this.weight;
      this.remaining_payment = this.freight - this.advance;
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
    get_consignor() {
      url = this.get_url(this.consignor_gstin, "CONSIGNOR");
      axios
        .get(url)
        .then((response) => {
          if (response.status === 200) {
            data = response.data;
            this.consignor_name = data.result.name;
            this.consignor_address = data.result.address;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    get_consignee() {
      url = this.get_url(this.consignee_gstin, "CONSIGNEE");
      axios
        .get(url)
        .then((response) => {
          if (response.status == 200) {
            data = response.data;
            this.consignee_name = data.result.name;
            this.consignee_address = data.result.address;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
