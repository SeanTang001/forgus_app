#' ui

#---------------------------
# Libraries Needed (Also add to DESCRIPTION)
#---------------------------
library(shiny)
library(shinythemes)
library(DT)
#library(shinyalert)
#library(shinyWidgets)
library(shinyTime)

#---------------------------
# ui object
#---------------------------

#library(shinydashboard)
#library(leaflet)




ui <- fluidPage(
  theme = "styles.css",
  tags$style(type="text/css",
             ".shiny-output-error { visibility: hidden; }",
             ".shiny-output-error:before { visibility: hidden; }"
  ),
  tags$script(src = "script.js"),
  tags$div(
    HTML('
    <script async defer
			src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA5aevdcRxbI2nBJ8UGTh_m7kESdN0AVqA&callback=initMap">
		</script>
    <script type="text/javascript" src="date.js"></script>
    ')
  ),
  titlePanel("Forgus: Foot Traffic Tracker"),
  fluidRow(
    column(6,
           br(),
           br(),
           br(),
           div(
             id="map",
             class="maps"
           )
           # div(
           #   height="200px",
           #   width="200px",
           #   style="overflow: true;!important position: relative;",
           # )
           ),
    column(6,
           tabsetPanel(
             type="tabs",
             tabPanel(
               textOutput("title"),
               br(),
               fluidRow(
                 column(3,                       
                        dateRangeInput("daterange", "Date range:")
                 ),
                 column(3,
                        timeInput("starttime", "Enter Start time")
                 ),
                 column(3,
                        timeInput("endtime", "Enter End time"),
                 ),
                 column(3,
                        selectInput("interval", label = "interval", choices = c("Year", "Month", "Day", "Hour", "Minute"))
                  )
               ),
               div(
                 class="table",
                 DTOutput(outputId = "table")
               ),
              div(
                 class="table",
                 plotOutput("trend"))
               )
             )
           
            )
          )
  )
