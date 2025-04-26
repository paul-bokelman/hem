import { useReactMediaRecorder } from "react-media-recorder";
import { toast } from "sonner";

export const useAudioRecorder = (uploadUrl: string) => {
  const { startRecording, stopRecording, mediaBlobUrl, clearBlobUrl } = useReactMediaRecorder({
    audio: true,
    onStop: async (blobUrl, blob) => {
      if (blob) {
        const formData = new FormData();
        formData.append("file", blob, "recording.webm");

        toast.promise(
          fetch(uploadUrl, {
            method: "POST",
            body: formData,
          }).then((response) => {
            if (!response.ok) {
              throw new Error("Failed to upload audio");
            }
            return response;
          }),
          {
            loading: "Uploading audio...",
            success: "Audio uploaded successfully!",
            error: "Audio upload failed. Please try again.",
          }
        );
      }
    },
  });

  return { startRecording, stopRecording, mediaBlobUrl, clearBlobUrl };
};
