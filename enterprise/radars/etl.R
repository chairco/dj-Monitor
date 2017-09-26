args <- commandArgs(TRUE)

if(FALSE){
  args[2] <- "CVDU01"
  args[1] <- "ETL"
}

# Set logger
library(logging)
logReset()
basicConfig(level='FINEST')

# sumulate ETL process stdout:
func_start_time.ETL_process <- Sys.time()
loginfo(paste0("[ETL_process][Start] : ", func_start_time.ETL_process))

func_name <- 'FDC_Import'
func_start_time.fdc_import <- Sys.time()
loginfo(paste0("[FDC_import][Start] : ", func_start_time.fdc_import))


func_name <- "Mea_Import"
func_start_time.mea_import <- Sys.time()
loginfo(paste0("[Mea_import][Start] : ", func_start_time.mea_import))
loginfo(paste0("[xy_complete_set_summary]"))
func_end_time.mea_import <- Sys.time()
loginfo(paste0("[Mea_import][End][Elapsed_time] : ", func_end_time.mea_import-func_start_time.mea_import))


func_name <- "FDC_Indicator"
loginfo(paste0("[FDC_Ind_Transform][Get_time_period]"))


func_name <- "FDC_Sync"
loginfo(paste0("[FDC_Sync][Get_time_period]"))


func_end_time.ETL_process <- Sys.time()
loginfo(paste0("[ETL_process][End][Elapsed_time] : ",func_end_time.ETL_process-func_start_time.ETL_process)) 