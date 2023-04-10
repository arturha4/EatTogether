const roomNumber = document.getElementsByName('room_number')[0];
console.log(roomNumber);
roomNumber.addEventListener("input", function (e){
     console.log(`value: ${roomNumber.value}`)
 })
console.log(roomNumber)