import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { BrandButton } from "#/components/features/settings/brand-button";
import { SettingsInput } from "#/components/features/settings/settings-input";
import { LoadingSpinner } from "#/components/shared/loading-spinner";
import { CreateApiKeyResponse } from "#/api/api-keys";
import {
  displayErrorToast,
  displaySuccessToast,
} from "#/utils/custom-toast-handlers";
import { ApiKeyModalBase } from "./api-key-modal-base";
import { useCreateApiKey } from "#/hooks/mutation/use-create-api-key";

interface CreateApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onKeyCreated: (newKey: CreateApiKeyResponse) => void;
}

export function CreateApiKeyModal({
  isOpen,
  onClose,
  onKeyCreated,
}: CreateApiKeyModalProps) {
  const { t } = useTranslation();
  const [newKeyName, setNewKeyName] = useState("");
  const [newKeyToken, setNewKeyToken] = useState("");

  const createApiKeyMutation = useCreateApiKey();

  const handleCreateKey = async () => {
    if (!newKeyName.trim() || !newKeyToken.trim()) {
      displayErrorToast(t(I18nKey.ERROR$REQUIRED_FIELD));
      return;
    }

    try {
      // Send both name and token
      const newKey = await createApiKeyMutation.mutateAsync({
        name: newKeyName,
        token: newKeyToken,
      });
      onKeyCreated(newKey);
      displaySuccessToast(t(I18nKey.SETTINGS$API_KEY_CREATED));
      setNewKeyName("");
      setNewKeyToken("");
    } catch (error) {
      displayErrorToast(t(I18nKey.ERROR$GENERIC));
    }
  };

  const handleCancel = () => {
    setNewKeyName("");
    setNewKeyToken("");
    onClose();
  };

  const modalFooter = (
    <>
      <BrandButton
        type="button"
        variant="primary"
        className="grow"
        onClick={handleCreateKey}
        isDisabled={createApiKeyMutation.isPending || !newKeyName.trim() || !newKeyToken.trim()}
      >
        {createApiKeyMutation.isPending ? (
          <LoadingSpinner size="small" />
        ) : (
          t(I18nKey.BUTTON$CREATE)
        )}
      </BrandButton>
      <BrandButton
        type="button"
        variant="secondary"
        className="grow"
        onClick={handleCancel}
        isDisabled={createApiKeyMutation.isPending}
      >
        {t(I18nKey.BUTTON$CANCEL)}
      </BrandButton>
    </>
  );

  return (
    <ApiKeyModalBase
      isOpen={isOpen}
      title={t(I18nKey.SETTINGS$CREATE_API_KEY)}
      footer={modalFooter}
    >
      <div data-testid="create-api-key-modal">
        <p className="text-sm text-gray-300">
          {t(I18nKey.SETTINGS$CREATE_API_KEY_DESCRIPTION)}
        </p>
        <SettingsInput
          testId="api-key-name-input"
          label={t(I18nKey.SETTINGS$NAME)}
          placeholder={t(I18nKey.SETTINGS$API_KEY_NAME_PLACEHOLDER)}
          value={newKeyName}
          onChange={(value) => setNewKeyName(value)}
          className="w-full mt-4"
          type="text"
        />
        <SettingsInput
          testId="api-key-token-input"
          label={t(I18nKey.SETTINGS$API_KEY_TOKEN_LABEL || "Token")}
          placeholder={t(I18nKey.SETTINGS$API_KEY_TOKEN_PLACEHOLDER || "Paste your token")}
          value={newKeyToken}
          onChange={(value) => setNewKeyToken(value)}
          className="w-full mt-4"
          type="password"
        />
      </div>
    </ApiKeyModalBase>
  );
}
