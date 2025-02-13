let clock;
let frequency;
let paused = false;
let onLight = false;

/* Switches */
function activateSwitch(switchComponent) {
  if (switchComponent.hasClass('on')) {
    switchComponent.removeClass('on');
    playAudio('switch-off.mp3');
  } else {
    switchComponent.addClass('on');
    playAudio('switch-on.mp3');
  }
  $('#activateSwitchComponent').addClass('hover').delay(400).queue(function (next) {
    $(this).removeClass('hover');
    next();
  });
}

function POWER() {
  return 1; // Always provides power
}
let onSwich = false
let lightAudioPlayed = {};
function process() {
  for (const component in diagram) {
    if (diagram[component].type === 'POWER') {
      diagram[component].outputs.output1.state = 1;
      diagram[component].outputs.output2.state = 1;
    }
    if (diagram[component].type === 'SWITCH') {
    // SWITCH Logic: Check input state and switch status
        let inputPower = diagram[component].inputs.input;
        if((inputPower.from[0].pin === "output1" || inputPower.from[0].pin === "output2" )){
          inputPower.state = 1;
        }else{
          inputPower.state = 0;
          inputPower.from=[];
        }
        onSwich = ($(`#${component}`).hasClass('on') ? true : false);
        const isSwitchOn = $(`#${component}`).hasClass('on') ? 1 : 0;
        for (const input of diagram[component].outputs.output.to) {
          if ($(`#${input.component}`).length) {
            diagram[input.component].inputs[input.pin].state = 1;
          } else {
            const arrayOutput = diagram[component].outputs.output.to;
            const indexOutput = arrayOutput.indexOf(input);
            arrayOutput.splice(indexOutput, 1);
          }
        }
    }
    
    if (diagram[component].type === 'AND') {
        //const inputs = Object.values(diagram[component].inputs).map(input => input.state);
      const inp1 = diagram[component].inputs.input1;
      const inp2 = diagram[component].inputs.input2;
      
        if (((inp2.from[0].pin === "output1" || inp2.from[0].pin === "output" ) && (inp1.from[0].pin === "output2" || inp1.from[0].pin === "output") && (onSwich)) || ((inp1.from[0].pin === "output2" && inp2.from[0].pin === "output1") && (inp1.from[0].component === inp2.from[0].component))) {
          $(`#${component}`).addClass('on');
          if (!lightAudioPlayed[component]) {
            // playAudio('electricity.mp3', `audio-${component}`, true);
            lightAudioPlayed[component] = true;
          }
        } else {
          $(`#${component}`).removeClass('on');
          $(`#audio-${component}`).remove();
          lightAudioPlayed[component] = false;
        }
    }
  }
}

changeFrequency();

function pauseClock() {
  if (paused) {
    clock = setInterval(process, frequency);
    $('#pauseBtn').find('.google-icon').text('stop');
    $('#pauseBtn').find('.stop-play-alt').text('Stop');
    paused = false;
  } else {
    clearInterval(clock);
    $('#pauseBtn').find('.google-icon').text('play_arrow');
    $('#pauseBtn').find('.stop-play-alt').text('Play');
    paused = true;
  }
}

function changeFrequency() {
  const value = $('input[name="frequency"]').val();
  $('#ClockFrequency').text(`${value} Hz  /  ${1000 / value} ms cycle`);

  clearInterval(clock);
  frequency = 1000 / value;
  if (!paused) {
    clock = setInterval(process, frequency);
  }
}
