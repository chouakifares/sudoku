// we use this function to draw the grid on the screen, we pass to this function a promise that return a Grid object
function drawGrid(grille){
	// we use this annonymous function to have access to the actual content of the promise 
	if(grille){
		grille.then(function(newGrid){
			//we make sure that our grid doesn't contain anything except a div containnig our buttons in the beginning of the element
			grid=document.getElementById("grille");
			if(grid.children.length>1){
				for (var i = grid.children.length - 1; i >=1; i--) {
					grid.removeChild(grid.children[i])
				}
			}
			for (var i = 0; i < 9; i++) {
				line=document.createElement("div");
				//some styling
				line.style.display="flex";
				for (var j = 0; j <9 ; j++) {
					cell=document.createElement("input");
					cell.class="cellule";
					cell.type="text";
					cell.style.fontSize="2em";
					cell.style.textAlign="center";
					cell.style.border="solid 1px gray";
					if(i==0 || i==3 || i==6){
						cell.style.borderTop="solid 2px black"
					}
					else if(i==8 || i==2 || i==5){
						cell.style.borderBottom="solid 2px black"
					}
					if(j==0 || j==3 || j==6){
						cell.style.borderLeft="solid 2px black"
					}
					else if(j==8 || j==2 || j==5){
						cell.style.borderRight="solid 2px black"
					}
					cell.style.height="40px";
					cell.style.width="40px";
					//we fill the grid with the elements contained in our Grid object's g attribute
					if(newGrid[i][j]){
						cell.value=newGrid[i][j];
						cell.disabled=true;
					}
					// we use this eventlistener for formatting text and making sure the text is valid
					cell.addEventListener("blur",function(e){
						e.target.value=e.target.value.replace(/\s/g, '');
						if(e.target.value.length>1) 	
							e.target.value=e.target.value[0];
						if(isNaN(e.target.value)){
							alert("incorrect value");
							e.target.value='';
						}
					})
					line.appendChild(cell);
				}
				grid.appendChild(line);
			}
		})
	}
	else{
		grid=document.getElementById("grille");
		//we make sure that our grid doesn't contain anything except a div containnig our buttons in the beginning of the element
		if(grid.children.length>1){
			for (var i = grid.children.length - 1; i >=1; i--) {
			grid.removeChild(grid.children[i])
			}
		}
		for (var i = 0; i < 9; i++) {
			line=document.createElement("div");
			//some styling
			line.style.display="flex";
			for (var j = 0; j <9 ; j++) {
				cell=document.createElement("input");
				cell.class="cellule";
				cell.type="text";
				cell.style.fontSize="2em";
				cell.style.textAlign="center";
				cell.style.border="solid 1px gray";
				if(i==0 || i==3 || i==6)
					cell.style.borderTop="solid 2px black"
				else if(i==8 || i==2 || i==5)
					cell.style.borderBottom="solid 2px black"
				if(j==0 || j==3 || j==6)
					cell.style.borderLeft="solid 2px black"
				else if(j==8 || j==2 || j==5)
					cell.style.borderRight="solid 2px black"
				cell.style.height="40px";
				cell.style.width="40px";
				// we use this eventlistener for formatting text and making sure the text is valid
				cell.addEventListener("blur",function(e){
					e.target.value=e.target.value.replace(/\s/g, '');
					if(e.target.value.length>1) 	
						e.target.value=e.target.value[0];
					if(isNaN(e.target.value)){
						alert("incorrect value");
						e.target.value='';
					}
				})
				line.appendChild(cell);
			}
			grid.appendChild(line);
		}
	}
}
//we use this function to verify the users grid
function verify(){
	grid=document.getElementById("grille");
	let current_grid=[];
	lines=grid.getElementsByTagName("div");
	//we loop trough the grid and look for user input
	// we start from 1 for i because the first div element contains the buttons which we are not interested in 
	for (var i = 1; i < lines.length; i++) {
		cells=lines[i].getElementsByTagName("input");
		for (var j = 0; j < cells.length; j++) {
			if(cells[j].value!='' && !cells[j].disabled){
				//once we found an actual cell that isn't disabled or empty (which means the user interacted with it)	
				// we call an anonymous function since this is a closure because pywebview.api requests are asynchronous 
				a=function(cells,line,column){
					pywebview.api.get_cell(line,column).then(function(val){		
						// we check if the value isn't correct then we change the bg color of the cell to red (means false)
						if(cells[column].value!=val)
							cells[column].style.backgroundColor='#f73131';
						// if not we change the bg color of the cell to green (means success)
						else
							cells[column].style.backgroundColor='#5cb85c';
						
					})
					// we pass i-1 instead of i since i started from 1
				}(cells,i-1,j);	
			}
		}
	}		
}