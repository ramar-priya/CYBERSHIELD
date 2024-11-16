function encodeMessage(imageData, message) {
  const data = imageData.data;
  const messageBinary =
    message
      .split("")
      .map((char) => char.charCodeAt(0).toString(2).padStart(8, "0"))
      .join("") + "1111111111111110"; // Add a delimiter
  let messageIndex = 0;

  for (
    let i = 0;
    i < data.length && messageIndex < messageBinary.length;
    i += 4
  ) {
    data[i] = (data[i] & 0xfe) | parseInt(messageBinary[messageIndex]); // Modify the red channel
    messageIndex++;
  }

  return imageData;
}

function decodeMessage(imageData) {
  const data = imageData.data;
  let binaryMessage = "";

  for (let i = 0; i < data.length; i += 4) {
    binaryMessage += (data[i] & 1).toString();
  }

  const messageParts = binaryMessage.split("1111111111111110");
  return messageParts[0]
    .match(/.{1,8}/g)
    .map((byte) => String.fromCharCode(parseInt(byte, 2)))
    .join("");
}

document.getElementById("encodeButton").addEventListener("click", () => {
  const imageInput = document.getElementById("imageInput");
  const messageInput = document.getElementById("messageInput");
  const outputCanvas = document.getElementById("outputCanvas");
  const ctx = outputCanvas.getContext("2d");

  if (imageInput.files && imageInput.files[0]) {
    const img = new Image();
    img.onload = () => {
      outputCanvas.width = img.width;
      outputCanvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, img.width, img.height);
      const encodedImageData = encodeMessage(imageData, messageInput.value);
      ctx.putImageData(encodedImageData, 0, 0);

      document.getElementById("downloadButton").style.display = "block";
    };
    img.src = URL.createObjectURL(imageInput.files[0]);
  }
});

document.getElementById("downloadButton").addEventListener("click", () => {
  const outputCanvas = document.getElementById("outputCanvas");
  const link = document.createElement("a");
  link.download = "encoded_image.png";
  link.href = outputCanvas.toDataURL();
  link.click();
});

document.getElementById("decodeButton").addEventListener("click", () => {
  const imageInput = document.getElementById("imageInput");
  const outputCanvas = document.getElementById("outputCanvas");
  const ctx = outputCanvas.getContext("2d");

  if (imageInput.files && imageInput.files[0]) {
    const img = new Image();
    img.onload = () => {
      outputCanvas.width = img.width;
      outputCanvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, img.width, img.height);
      const decodedMessage = decodeMessage(imageData);
      document.getElementById("decodedMessage").innerText = decodedMessage;
    };
    img.src = URL.createObjectURL(imageInput.files[0]);
  }
});
