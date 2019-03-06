// Funtion for limiting the amount of checked boxes
function checkboxlimit(checkgroup, limit){
	var checkgroup=checkgroup
	var limit=limit
	for (var i=0; i<checkgroup.length; i++){
		checkgroup[i].onclick=function(){
		var checkedcount=0
		for (var i=0; i<checkgroup.length; i++)
			checkedcount+=(checkgroup[i].checked)? 1 : 0
		if (checkedcount>limit){
			alert("You can only select a maximum of "+limit+" topping(s) with that item")
			this.checked=false
			}
		}
	}
}

document.addEventListener('DOMContentLoaded', () => {
	let toppings = document.querySelector("#pizza").topping_selection
	// Setting the allowed toppings to 0 by default
	checkboxlimit(toppings, 0)

	pizza_choice = document.getElementById("pizza_selection")

	//  Changing the no. of allowed toppings according to selected item
	pizza_choice.addEventListener("change", () => {

		// Clear topping selection when item changed
		for (var i=0; i<toppings.length; i++) {
			toppings[i].checked = false;
		}
	  if (pizza_choice.value == 2 || pizza_choice.value == 7) {
	    toppings[0].checked = true;
	    checkboxlimit(toppings, 1)
	  }
	  else if (pizza_choice.value == 3 || pizza_choice.value == 8) {
	    toppings[0].checked = true;
			toppings[1].checked = true;
	    checkboxlimit(toppings, 2)
	  }
	  else if (pizza_choice.value == 4 || pizza_choice.value == 9) {
			toppings[0].checked = true;
			toppings[1].checked = true;
			toppings[2].checked = true;
	    checkboxlimit(toppings, 3)
	  }
	  else if (pizza_choice.value == 5 || pizza_choice.value == 10) {
			alert("You can have upto 5 toppings on a Special Pizza!")
	    console.log('Special')
			for (var i=0; i<5; i++) {
				toppings[i].checked = true;
			}
	    checkboxlimit(toppings, 5)
	  }
	})

	//  Disabling the small option for the sub that only comes in large size
	sub_choice = document.getElementById('sub_selection')
	sub_choice.addEventListener("change", () => {
		let small_size = document.getElementById('sub_size_choice_small');
		let large_size =  document.getElementById('sub_size_choice_large');
	  if (sub_choice.value == 11) {
	    small_size.disabled = true;
	    small_size.checked = false;
	    large_size.checked = true;
		}
		else {
			small_size.disabled = false;
			small_size.checked = true;
		}
	})
	})
