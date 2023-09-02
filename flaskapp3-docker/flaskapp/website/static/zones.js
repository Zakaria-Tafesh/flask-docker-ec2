// document.addEventListener("DOMContentLoaded", function() {
//     const editButtons = document.querySelectorAll(".edit-button");
//     const deleteButtons = document.querySelectorAll(".delete-button");
//
//     editButtons.forEach((button, index) => {
//         button.addEventListener("click", () => {
//             // Here you can implement your edit functionality
//             alert(`Editing row ${index + 1}`);
//         });
//     });
//
//     deleteButtons.forEach((button, index) => {
//         button.addEventListener("click", () => {
//             // Here you can implement your delete functionality
//             if (confirm("Are you sure you want to delete this row?")) {
//                 // button.closest("tr").remove();
//
//             }
//         });
//     });
// });

function deleteZone(zoneId) {
    if (confirm("Are you sure you want to delete this Zone?")) {
                // button.closest("tr").remove();
        fetch("/delete-zone", {
        method: "POST",
        body: JSON.stringify({ zoneId: zoneId }),
        }).then((_res) => {
        window.location.href = "/";
        });
            }

  }

function updateZone1(zoneId) {
    // let elements = document.getElementsByName("fname");
    // alert('Hello ' + zoneId);


    // document.getElementById("client_name").innerHTML = zoneId ;

    fetch("/update-zone1", {
    method: "POST",
    body: JSON.stringify({ zoneId: zoneId }),
    }).then(response => response.json()).then(data => {
        // alert('Hello ' + data);
        document.getElementById("client_name").value = data['client_name'] ;
        document.getElementById("url").value = data['url'] ;
        document.getElementById("payload").value = data['payload'] ;
        document.getElementById("zone_id").value = zoneId ;


        document.getElementById("update-zone").style.display = "block";
        document.getElementById("cancel").style.display = "block";
        document.getElementById("add-zone").style.display = "none";

        let pageBottom = document.querySelector("#zone_id");
        pageBottom.scrollIntoView();

    }) ;


}

function updateZone2() {
    let zone_id = document.getElementById("zone_id").innerHTML;
    let client_name = document.getElementById("client_name").value;
    let url = document.getElementById("url").value;
    let payload = document.getElementById("payload").value;
    alert('Zone : ' + zone_id + client_name + url +  payload);

    fetch("/update-zone2", {
    method: "POST",
    body: JSON.stringify({ zone_id: zone_id,
        client_name: client_name,
        url: url,
        payload: payload,

    }),
    }).then(response => response.json()).then(data => {
        // alert('Hello ' + data);
        document.getElementById("client_name").value = "" ;
        document.getElementById("url").value = "" ;
        document.getElementById("payload").value = "" ;
        document.getElementById("zone_id").value = "" ;


        document.getElementById("update-zone").style.display = "none";
        document.getElementById("cancel").style.display = "none";
        document.getElementById("add-zone").style.display = "block";

        let home = document.querySelector("#home");
        window.location.href = "/";
        home.scrollIntoView();

    }) ;


}

function myCancel() {
        // document.getElementById("client_name").innerHTML = "" ;
        document.getElementById("client_name").value = "" ;
        // document.getElementById("url").innerHTML = "" ;
        document.getElementById("url").value = "" ;
        // document.getElementById("payload").innerHTML = "" ;
        document.getElementById("payload").value = "" ;
        // document.getElementById("zone_id").innerHTML = "" ;
        document.getElementById("zone_id").value = "" ;


        document.getElementById("update-zone").style.display = "none";
        document.getElementById("cancel").style.display = "none";
        document.getElementById("add-zone").style.display = "block";

        let home = document.querySelector("#home");
        home.scrollIntoView();



}
