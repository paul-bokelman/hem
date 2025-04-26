import React, { useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Mic } from "lucide-react";
import { useAudioRecorder } from "@/hooks/use-audio-recorder";

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = React.useState(false);
  const { startRecording, stopRecording, mediaBlobUrl } = useAudioRecorder("http://localhost:5000/upload");
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
    if (mediaBlobUrl && audioRef.current) {
      audioRef.current.load();
      audioRef.current.play();
    }
  }, [mediaBlobUrl]);

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

      {mediaBlobUrl && (
        <audio ref={audioRef} src={mediaBlobUrl} className="w-full hidden">
          Your browser does not support the audio element.
        </audio>
      )}
    </div>
  );
};

export default AudioRecorder;
