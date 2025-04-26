import React from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import { useUser } from "@/partials/user-context";
import { toast } from "sonner";

export const useAudioRecorder = () => {
  const { user } = useUser();
  const { startRecording, stopRecording, mediaBlobUrl, clearBlobUrl } = useReactMediaRecorder({
    audio: true,
    onStop: async (blobUrl, blob) => {
      if (blob) {
        const formData = new FormData();
        formData.append("file", blob, "recording.webm");

        toast.promise(
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/respond`, {
            method: "POST",
            body: formData,
            headers: { "X-User-ID": user?.id || "" },
          }).then((response) => {
            if (!response.ok) {
              throw new Error("Failed to upload audio");
            }

            response.blob().then((audioBlob) => {
              const audioUrl = URL.createObjectURL(audioBlob);
              setProcessedAudioUrl(audioUrl);
            });
          }),
          {
            loading: "Uploading and processing audio...",
            error: "Audio processing failed. Please try again.",
          }
        );
      }
    },
  });
  const [processedAudioUrl, setProcessedAudioUrl] = React.useState<string | null>(null);
  return { startRecording, stopRecording, mediaBlobUrl, clearBlobUrl, processedAudioUrl };
};
