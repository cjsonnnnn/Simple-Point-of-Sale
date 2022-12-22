<script>
import { RouterLink, RouterView } from 'vue-router'
import quantityInput from './components/quantityInput.vue';
import invoice from './components/invoice.vue'

export default {
  components: { quantityInput, invoice }
}
</script>

<template>
  <div class="text-center mt-5">
    <h1>Simple To-do List Program</h1>
  </div>


  <div class="container-fluid">
    <div class="row" style="height: 720px">
      <invoice></invoice>

      <!-- right area -->
      <div class="col-9 bg-warning d-flex flex-column flex-wrap">
        <!-- categories -->
        <div class="row bg-success text-center overflow-auto">
          <div class="bg-danger m-2 p-2" style="width: 90px; border-radius: 9px;">3123</div>
          <div class="bg-danger m-2 p-2" style="width: 90px; border-radius: 9px;">3123</div>
          <div class="bg-danger m-2 p-2" style="width: 90px; border-radius: 9px;">3123</div>
        </div>

        <!-- products -->
        <div class="row bg-danger flex-fill">
          <div class="container-fluid overflow-auto" style="height: 630px">
            <div class="row overflow-auto">
              <!-- a product -->
              <div class="col-3 p-2">
                <div class="card" style="width: 100%;">
                  <img
                    src="https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=300"
                    class="card-img-top" alt="...">
                  <div class="card-body">
                    <!-- item name -->
                    <div>Kamera 1</div>

                    <!-- item price and qty -->
                    <div class="container-fluid mt-1">
                      <div class="row p-0 d-flex flex-column align-items-end">
                        <!-- price -->
                        <div class="col-12 p-0 d-flex align-items-center">Rp. 30.000</div>

                        <!-- quantity input -->
                        <div class="col-7 p-0 mt-2">
                          <quantityInput></quantityInput>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>


        </div>

        <!-- admin commands -->
        <div class="row m-2" style="height: 45px">
          <div class="col-12 d-flex justify-content-center bg-danger">
            <button type="button" class="btn btn-primary p-2" style="width: 72%;">Sale Report</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>