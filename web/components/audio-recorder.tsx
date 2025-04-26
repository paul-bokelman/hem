import React, { useRef, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Mic } from "lucide-react";
import { useAudioRecorder } from "@/hooks/use-audio-recorder";

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const { startRecording, stopRecording, processedAudioUrl } = useAudioRecorder();
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handleRecord = () => {
    if (isRecording) {
      stopRecording();
      setIsRecording(false);
    } else {
      startRecording();
      setIsRecording(true);
    }
  };

  useEffect(() => {
    const playAudio = async () => {
      if (processedAudioUrl && audioRef.current) {
        audioRef.current.src = processedAudioUrl;
        audioRef.current.load();
        await audioRef.current.play();
      }
    };
    playAudio();
  }, [processedAudioUrl]);

  return (
    <div className="mt-2 w-fit flex flex-col items-start gap-2">
      <Button
        variant="outline"
        className={`w-fit border ${isRecording ? "!border-red-500 !bg-red-500/10 !text-red-500" : ""}`}
        onClick={handleRecord}
      >
        <Mic className={`mr-2 h-4 w-4 ${isRecording ? "text-red-500" : ""}`} />
        {isRecording ? "Stop Recording" : "Record"}
      </Button>

      <audio ref={audioRef} className="w-full hidden">
        Your browser does not support the audio element.
      </audio>
    </div>
  );
};

export default AudioRecorder;
