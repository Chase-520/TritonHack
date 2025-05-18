<script>
  var connectContainer = document.getElementById("connectContainer");
  if (connectContainer) {
    connectContainer.addEventListener("click", function () {
      document.getElementById("heartRate").classList.remove("hidden");
      document.getElementById("heartRateNumber").classList.remove("hidden");
      document.getElementById("bloodPressure").classList.remove("hidden");
      document.getElementById("bloodPressureNumber").classList.remove("hidden");
    })
  }
</script>
