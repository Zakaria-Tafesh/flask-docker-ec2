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
    alert('Hello ' + zoneId);
    document.getElementById("client_name").innerHTML = zoneId ;

    // fetch("/delete-zone", {
    // method: "POST",
    // body: JSON.stringify({ zoneId: zoneId }),
    // }).then((_res) => {
    // window.location.href = "/";
    // });


}
