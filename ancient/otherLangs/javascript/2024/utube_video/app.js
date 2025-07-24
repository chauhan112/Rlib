let player;
let skipTimes = [];
let currentSkip = { start: null, end: null };

function onYouTubeIframeAPIReady() {
  // Initially, the player will be created when a URL is entered and the loadVideo function is called
}

function loadVideo() {
  const url = document.getElementById("video-url").value;
  const videoId = extractVideoId(url);
  if (videoId) {
    if (player) {
      player.loadVideoById(videoId);
    } else {
      player = new YT.Player("player", {
        videoId: videoId,
        events: {
          onReady: onPlayerReady,
          onStateChange: onPlayerStateChange,
        },
      });
    }
  } else {
    alert("Please enter a valid YouTube URL.");
  }
}

function extractVideoId(url) {
  const regex =
    /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

function onPlayerReady(event) {
  event.target.playVideo();
}

function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING) {
    checkSkipTimes();
  }
}

function checkSkipTimes() {
  let currentTime = player.getCurrentTime();

  for (const element of skipTimes) {
    if (currentTime >= element.start && currentTime < element.end) {
      player.seekTo(element.end, true);
      break;
    }
  }

  setTimeout(checkSkipTimes, 1000);
}

function markSkipStart() {
  currentSkip.start = player.getCurrentTime();
}

function markSkipEnd() {
  currentSkip.end = player.getCurrentTime();
}

function saveSkipTimes() {
  if (currentSkip.start !== null && currentSkip.end !== null) {
    skipTimes.push({ ...currentSkip });
    displaySkipTimes();
    currentSkip = { start: null, end: null };
  } else {
    alert("Please mark both start and end times before saving.");
  }
}

function displaySkipTimes() {
  const skipTimesDiv = document.getElementById("skip-times");
  skipTimesDiv.innerHTML = "";
  skipTimes.forEach((skip, index) => {
    const div = document.createElement("div");
    div.classList.add("skip-time");
    div.innerHTML = `
            <input type="number" value="${skip.start}" onchange="updateSkipStart(${index}, this.value)">
            <input type="number" value="${skip.end}" onchange="updateSkipEnd(${index}, this.value)">
            <button onclick="removeSkipTime(${index})">Remove</button>
        `;
    skipTimesDiv.appendChild(div);
  });
}

function updateSkipStart(index, value) {
  skipTimes[index].start = parseFloat(value);
}

function updateSkipEnd(index, value) {
  skipTimes[index].end = parseFloat(value);
}

function removeSkipTime(index) {
  skipTimes.splice(index, 1);
  displaySkipTimes();
}
