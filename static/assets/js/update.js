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
        consignee_address: ""
      };
    },
    mounted() {
        const url_string = window.location.pathname;
        const id = url_string.split('/').pop();
        base_url = window.location.origin;
        url =
          base_url + "/consignment/details?id=" + id
        axios
            .get(url)
            .then(response => {
                if (response.status === 200) {
                    data = response.data
                    this.consignor_gstin = data.consignor_gstin
                    this.get_consignor()
                    this.consignee_gstin = data.consignee_gstin
                    this.get_consignee()
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
        this.remaining_payment = data.remaining_payment
        this.advance = data.advance
        
      },
      calculate_freight() {
        this.freight = this.rate * this.weight;
        this.freight = this.round_of(this.freight);
        this.remaining_payment = this.freight - this.advance;
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
      round_of(val) {
        return Number((val).toFixed(2))
      }
    },
  });
  