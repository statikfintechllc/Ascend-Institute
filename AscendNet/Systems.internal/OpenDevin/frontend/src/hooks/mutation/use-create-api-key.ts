import { useMutation, useQueryClient } from "@tanstack/react-query";
import ApiKeysClient, { CreateApiKeyResponse } from "#/api/api-keys";
import { API_KEYS_QUERY_KEY } from "#/hooks/query/use-api-keys";

/**
 * Determines if the given key name implies a local-only context (e.g., Ollama, Mistral).
 */
function isLocalModelKey(name: string): boolean {
  const lowered = name.toLowerCase();
  return (
    lowered.includes("ollama") ||
    lowered.includes("mistral") ||
    lowered.includes("local") ||
    lowered.includes("localhost") ||
    lowered.includes("gpu")
  );
}

export function useCreateApiKey() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (name: string): Promise<CreateApiKeyResponse> => {
      if (isLocalModelKey(name)) {
        // Simulate a fake key to keep the flow alive for local usage
        return {
          id: `local-${Date.now()}`,
          key: `local-${crypto.randomUUID()}`,
          name,
          created_at: new Date().toISOString(),
          last_used_at: null,
        };
      }

      return ApiKeysClient.createApiKey(name);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [API_KEYS_QUERY_KEY] });
    },
  });
}
