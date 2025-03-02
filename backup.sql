PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
/****** CORRUPTION ERROR *******/
/****** database disk image is malformed ******/
/****** ERROR: near "ORDER": syntax error ******/
CREATE TRIGGER AC_delete_cabinetsAdditionalData_on_cabinet_removed AFTER DELETE ON Cabinets BEGIN DELETE FROM CabinetsAdditionalData WHERE CabinetsAdditionalData.CabinetId = OLD.CabinetId; END;
CREATE TRIGGER AC_delete_additionalData_on_speakerId_changed AFTER UPDATE OF SpeakerId ON Cabinets BEGIN DELETE FROM CabinetsAdditionalData WHERE CabinetsAdditionalData.CabinetId = OLD.CabinetId; DELETE FROM SourceGroupsAdditionalData WHERE SourceGroupsAdditionalData.SourceGroupId = OLD.SourceGroupId; END;
CREATE TRIGGER AC_delete_sourceGroupsAdditionalData_on_sourceGroup_removed AFTER DELETE ON SourceGroups BEGIN DELETE FROM SourceGroupsAdditionalData WHERE SourceGroupsAdditionalData.SourceGroupId = OLD.SourceGroupId; END;
CREATE TRIGGER AC_delete_ArrayProcessingSlotsAdditionalData_on_ArrayProcessingSlot_removed AFTER DELETE ON ArrayProcessingSlots BEGIN DELETE FROM ArrayProcessingSlotsAdditionalData WHERE ArrayProcessingSlotsAdditionalData.ArrayProcessingSlotId = OLD.ArrayProcessingSlotId; END;
CREATE TRIGGER AC_delete_ArrayProcessingDataAdditionalData_on_ArrayProcessingSlot_removed AFTER DELETE ON ArrayProcessingData BEGIN DELETE FROM ArrayProcessingDataAdditional WHERE ArrayProcessingDataAdditional.ArrayProcessingSlotId = OLD.ArrayProcessingSlotId AND ArrayProcessingDataAdditional.CabinetId = OLD.CabinetId; END;
CREATE TRIGGER AC_delete_ArrayProcessingPlaneOffsets_on_VenueObject_removed AFTER DELETE ON VenueObjects BEGIN DELETE FROM ArrayProcessingPlaneOffsets WHERE ArrayProcessingPlaneOffsets.VenueObjectId = OLD.VenueObjectId; END;
CREATE TRIGGER AC_delete_PatchIO_on_Device_removed AFTER DELETE ON Devices BEGIN DELETE FROM PatchIOChannels WHERE PatchIOChannels.DeviceId = OLD.DeviceId; DELETE FROM PatchIOConnectors WHERE PatchIOConnectors.PatchInPortDeviceId = OLD.DeviceId OR PatchIOConnectors.PatchOutPortDeviceId = OLD.DeviceId; DELETE FROM PatchIOConnectors WHERE PatchIOConnectors.AmplifierDeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_unasssign_Controls_on_AmplifierChannels_removed AFTER DELETE ON AmplifierChannels FOR EACH ROW BEGIN UPDATE Controls SET TargetId = 0, TargetChannel = -1 WHERE TargetType = 2 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.AmplifierChannel; END;
CREATE TRIGGER R1_unasssign_Controls_on_MatrixInputs_removed AFTER DELETE ON MatrixInputs FOR EACH ROW BEGIN UPDATE Controls SET TargetId = 0, TargetChannel = -1 WHERE TargetType = 2 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.MatrixInput; END;
CREATE TRIGGER R1_unasssign_Controls_on_MatrixOutputs_removed AFTER DELETE ON MatrixOutputs FOR EACH ROW BEGIN UPDATE Controls SET TargetId = 0, TargetChannel = -1 WHERE TargetType = 2 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.MatrixOutput; END;
CREATE TRIGGER R1_unasssign_SceneTransportControls_on_Devices_removed AFTER DELETE ON Devices FOR EACH ROW BEGIN UPDATE Controls SET TargetId = 0, TargetChannel = 0 WHERE TargetType = 7 AND TargetId = OLD.DeviceId; END;
CREATE TRIGGER R1_unasssign_SceneControls_on_Scenes_removed AFTER DELETE ON Scenes FOR EACH ROW BEGIN UPDATE Controls SET TargetId = 0, TargetChannel = -1 WHERE TargetType = 6 AND TargetId = OLD.SceneId; END;
CREATE TRIGGER R1_delete_DevicesAmplifier_on_Devices_removed AFTER DELETE ON Devices FOR EACH ROW BEGIN DELETE FROM DevicesAmplifier WHERE DeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_delete_DevicesMatrix_on_Devices_removed AFTER DELETE ON Devices FOR EACH ROW BEGIN DELETE FROM DevicesMatrix WHERE DeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_delete_AmplifierChannels_on_DevicesAmplifier_removed AFTER DELETE ON DevicesAmplifier FOR EACH ROW BEGIN DELETE FROM AmplifierChannels WHERE DeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_delete_MatrixInputs_on_DevicesMatrix_removed AFTER DELETE ON DevicesMatrix FOR EACH ROW BEGIN DELETE FROM MatrixInputs WHERE DeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_delete_MatrixOutputs_on_DevicesMatrix_removed AFTER DELETE ON DevicesMatrix FOR EACH ROW BEGIN DELETE FROM MatrixOutputs WHERE DeviceId = OLD.DeviceId; END;
CREATE TRIGGER R1_delete_Groups_on_AmplifierChannels_removed AFTER DELETE ON AmplifierChannels FOR EACH ROW BEGIN DELETE FROM Groups WHERE Type = 1 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.AmplifierChannel; END;
CREATE TRIGGER R1_delete_Groups_on_MatrixInputs_removed AFTER DELETE ON MatrixInputs FOR EACH ROW BEGIN DELETE FROM Groups WHERE Type = 2 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.MatrixInput; END;
CREATE TRIGGER R1_delete_Groups_on_MatrixOutputs_removed AFTER DELETE ON MatrixOutputs FOR EACH ROW BEGIN DELETE FROM Groups WHERE Type = 3 AND TargetId = OLD.DeviceId AND TargetChannel = OLD.MatrixOutput; END;
CREATE TRIGGER R1_delete_SnapshotValues_on_AmplifierChannels_removed AFTER DELETE ON AmplifierChannels FOR EACH ROW BEGIN DELETE FROM SnapshotValues WHERE SnapshotTargetType = 0 AND TargetId = OLD.DeviceId AND TargetNode = OLD.AmplifierChannel; END;
CREATE TRIGGER R1_delete_SnapshotValues_on_MatrixInputs_removed AFTER DELETE ON MatrixInputs FOR EACH ROW BEGIN DELETE FROM SnapshotValues WHERE SnapshotTargetType = 0 AND TargetId = OLD.DeviceId AND TargetNode = OLD.MatrixInput; END;
/**** ERROR: (11) database disk image is malformed *****/
COMMIT;
