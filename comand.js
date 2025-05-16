
$("#start-btn").click(function() {
  eel.takecommand(); // Call the Python-exposed function via Eel
});
console.log("Calling backend...");
eel.start_jarvis()().then(() => {
  console.log("Backend responded");
});

 
