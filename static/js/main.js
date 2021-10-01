const popModal = () => {
  const text = $("#for-modal").val();
  let url = "/message";

  var xhr = new XMLHttpRequest();
  xhr.open("PUT", url);
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Authorization", "Bearer");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 201) {
      console.log(xhr.status);
      console.log(xhr.responseText);
      data = JSON.parse(xhr.responseText);
      alert(data["message"]);
    }
  };

  var data = `{"message": "${text}"}`;
  xhr.send(data);
};
