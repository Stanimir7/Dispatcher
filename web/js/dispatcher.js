$(document).ready(function () {
     $(".button-collapse").sideNav();
     $('.modal').modal({dismissible: false});
  });


//Why the hell isn't this built in w/ jquery?????
function objectifyForm(formArray) {//serialize data function

  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
    returnArray[formArray[i]['name']] = formArray[i]['value'];
  }
  return returnArray;
}