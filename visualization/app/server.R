library(shiny)
library(ggplot2)
library(dplyr)
library(cowplot)
library(tools)
library(RCurl)
library(zip)
library(tmap)
library(plyr)
library(broom)
library(lubridate)


options(shiny.maxRequestSize=100*1024^2)
pal_all <- argus::mappings()$pal_all

server <- function(input, output, session) {
  dataDefault <- argus::exampleData
  ggplottheme <- ggplot2::theme_bw()

timedata <- '[
	{"time":"2021-02-28T13:23:01.000Z"},
	{"time":"2021-02-28T14:24:04.000Z"},
	{"time":"2021-02-28T16:25:03.000Z"},
	{"time":"2021-02-28T17:26:05.000Z"},
	{"time":"2021-02-28T19:27:11.000Z"},
	{"time":"2021-03-01T20:28:11.000Z"},
	{"time":"2021-03-01T20:29:11.000Z"},
	{"time":"2021-03-01T20:30:05.000Z"},
	{"time":"2021-03-01T21:31:11.000Z"},
	{"time":"2021-03-01T22:32:05.000Z"},
	{"time":"2021-03-01T23:33:11.000Z"},
	{"time":"2021-03-01T23:34:05.000Z"},
	{"time":"2021-03-02T13:23:01.000Z"},
	{"time":"2021-03-02T14:24:04.000Z"},
	{"time":"2021-03-02T16:25:03.000Z"},
	{"time":"2021-03-02T17:26:05.000Z"},
	{"time":"2021-03-02T19:27:11.000Z"},
	{"time":"2021-03-02T20:28:11.000Z"},
	{"time":"2021-03-02T20:29:11.000Z"},
	{"time":"2021-03-02T20:30:05.000Z"},
	{"time":"2021-03-02T21:31:11.000Z"},
	{"time":"2021-03-02T22:32:05.000Z"},
	{"time":"2021-03-02T23:33:11.000Z"},
	{"time":"2021-03-02T23:34:05.000Z"}
]'

  settings <- reactive({data.frame()})
  settingsVars <- c("urlSelect",
                    "regionsSelect",
                    "scenariosSelect",
                    "scenarioRefSelect",
                    "paramsSelect")

  observeEvent(input$selectedLocation, {
    print("button has pressed")
    print(input$selectedLocation)
  })
  
  observeEvent(input$startdate, {
   #print(strftime(input$startdate, "%Y-%m-%d"))
    print(strftime(input$starttime, "%T"))
    print(strftime(input$endtime, "%T"))
    #print(strftime(input$enddate, "%Y-%m-%d"))
    print(typeof(input$daterange))
    print(class(input$daterange))
    print(input$daterange)
    print(input$daterange[[1]])
  })
  
  output$title <- renderText({ 
    input$selectedLocation
  })
  
  output$table <- renderDT(
    datax(),
    filter = "top"
  )
  output$trend <- renderPlot(
    plotz()
  )
  
  
  plotz <- reactive({
    print(input$interval)
    
    start<-paste(strftime(input$daterange[[1]], "%Y-%m-%d"),"T",
    strftime(input$starttime, "%T"),collapse=NULL, sep="")
    end<-paste(strftime(input$daterange[[2]], "%Y-%m-%d"),"T",
          strftime(input$endtime, "%T"),collapse=NULL, sep="")
    print(start)
    print(end)
    start<-as.POSIXct(start, format='%Y-%m-%dT%H:%M:%S')
    end<-as.POSIXct(end,format='%Y-%m-%dT%H:%M:%S') + 3*60*60
    print(start) 
    print(end)
    #    print(datax())
        ggplot2::ggplot(trendbyinterval(input$interval),
                      aes(x=x, y=n))+
        #                    lubridate::as_datetime(datax()$dateobj),y=1, size=5))+
        geom_line( color="steelblue") +
        geom_point() +
        geom_col()+
        scale_x_continuous(expand=c(start,start), limits=c(start,end))+
        geom_smooth(method="lm", formula=y~x^2) +
        # stat_poly_eq(parse=T, aes(label = ..eq.label..), formula=y~x)+
        stat_smooth(method = "glm", col = "red", fullrange=TRUE)+
        stat_smooth(method = "auto", col = "red", fullrange=TRUE)+
        xlab("time") +
        ylab("traffic") +
        theme(axis.text.x=element_text(angle=60, hjust=1),text=element_text(size=15))+
        xlim(start,end)
          
#        scale_x_datetime(date_breaks = paste("1 ", input$interval, collapse = NULL, sep='')) +
  })
  
  
  data <- function(){
    a <- jsonlite::fromJSON("http://127.0.0.1:8000/f")
    if (is.null(input$selectedLocation)){
      return(a$data[["test_location"]])
    }
    print(a$data[[input$selectedLocation]])
    return(a$data[[input$selectedLocation]])
  }
  
  
  datax <- function(){
    if (is.null(input$selectedLocation)){
      df
      return()      
    }
    request = paste("http://127.0.0.1:8000/d/",
                    input$selectedLocation,
                    "/",
                    strftime(input$daterange[[1]], "%Y-%m-%d"),"T",
                    strftime(input$starttime, "%T"),
                    "/",
                    strftime(input$daterange[[2]], "%Y-%m-%d"),"T",
                    strftime(input$endtime, "%T"), collapse = NULL, sep='')
    print(request)
    a <- jsonlite::fromJSON(request)$data
    a <- datetime(a)
    return(a) 
  }
  
  datetime <- function(a){
    a %>% dplyr::mutate(dateobj = as.POSIXct(a$time, format='%Y-%m-%dT%H:%M:%S')) -> a
    
    return(a %>% dplyr::mutate(year = strftime(a$time, format='%Y')) 
    %>% dplyr::mutate(month = strftime(a$time, format='%Y-%m'))    
    %>% dplyr::mutate(day = strftime(a$time, format='%Y/%m/%d'))
    %>% dplyr::mutate(hour = strftime(a$dateobj, format='%Y/%m/%dT%H'))
    %>% dplyr::mutate(minute = strftime(a$dateobj, format='%Y/%m/%dT%H:%M')))
  }
 
 trendbyinterval <- function(interval){
	 if (interval=="Minute"){
		 res <- datetime(datax()) %>% dplyr::count(minute)
		 res <- res %>% dplyr::mutate(x=as.POSIXct(res$minute, format='%Y/%m/%dT%H:%M'))
		 print(res)
		 return(res)
		 }
	 if (interval=="Hour"){
		 res <- datetime(datax()) %>% dplyr::count(hour)
		 res <- res %>% dplyr::mutate(x=as.POSIXct(res$hour, format='%Y/%m/%dT%H'))
		 print(res)
		 return (res) 	 
		 }		 
	 if (interval=="Day"){
		 res <- datetime(datax()) %>% dplyr::count(day)
		 res <- res %>% dplyr::mutate(x=as.POSIXct(res$day, format='%Y/%m/%d'))
		 print(res)
		 return(res)
		 }	 
	 if (interval=="Month"){
		 res <- datetime(datax()) %>% dplyr::count(month)
		 res <- res %>% dplyr::mutate(x=as.POSIXct(res$month, format='%Y-%m'))
		 print(res)
		 return(res)
		 }	 
	 if (interval=="Year"){
		 res <- datetime(datax()) %>% dplyr::count(year)
		 res <- res %>% dplyr::mutate(x=as.POSIXct(res$year, format='%Y'))
		 print(res)
		 return(res)
		 }	 
	 }

  
  observeEvent(input$loadsetting, {
    showModal(
      modalDialog(
        size = "s",
        easyClose = TRUE,
        footer = NULL,
        fileInput(
          inputId = "settingdata",
          label = "Upload csv",
          accept = c(".csv"),
          multiple = TRUE,
          width = "100%"
        ),
        fluidRow(
          column(6,
                 div(downloadButton(
                   outputId='downloadSettings',
                   label="Save Settings",
                   download = "settings.csv",
                   class = "download_button"),
                   style = "float:center"
                 ))
          ,
          column(6,
                 div(actionLink(inputId='defaultsetting',
                                label='Default Setting',
                                class = "btn btn-default shiny-download-link download_button",
                                icon = icon("cog","fa-1x")
                 )
                 )
          )
        )
      )
    )
  })
}

