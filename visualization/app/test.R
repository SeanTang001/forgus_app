library(ggplot2)
library(jsonlite)
library(dplyr)

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

  datax <- function(){
    a <- jsonlite::fromJSON(timedata)
    a <- datetime(a)
    return(a) 
  }
  

  datetime <- function(a){
    a %>% dplyr::mutate(dateobj = as.POSIXct(a$time, format='%Y-%m-%dT%H:%M:%S')) -> a
    
    return(a %>% dplyr::mutate(year = strftime(a$time, format='%Y')) 
    %>% dplyr::mutate(month = strftime(a$time, format='%Y/%m'))    
    %>% dplyr::mutate(day = strftime(a$time, format='%Y/%m/%d'))
    %>% dplyr::mutate(hour = strftime(a$dateobj, format='%Y/%mT%H'))
    %>% dplyr::mutate(minute = strftime(a$dateobj, format='%Y/%mT%H:%M')))
  }
 
 trendbyinterval <- function(interval){
	 if (interval=="minute"){
		 res <- datetime(datax()) %>% dplyr::count(minute)
		 res <- res %>% dplyr::mutate(x=res$hour)
		 return(res)
		 }
	 if (interval=="hour"){
		 res <- datetime(datax()) %>% dplyr::count(hour)
		 res <- res %>% dplyr::mutate(x=res$hour)
		 return (res) 	 
		 }		 
	 if (interval=="day"){
		 res <- datetime(datax()) %>% dplyr::count(day)
		 res <- res %>% dplyr::mutate(x=res$day)
		 return(res)
		 }	 
	 if (interval=="month"){
		 res <- datetime(datax()) %>% dplyr::count(month)
		 res <- res %>% dplyr::mutate(x=res$month)
		 return(res)
		 }	 
	 if (interval=="year"){
		 res <- datetime(datax()) %>% dplyr::count(year)
		 res <- res %>% dplyr::mutate(x=res$year)
		 return(res)
		 }	 
	 }


summaryPlot <- function(data){
	print(data)
    ggplot2::ggplot(data,
                    aes(x=x,y=n))+
      geom_point()+
      ggplottheme +
      ylab(NULL) +  xlab(NULL) +
#      facet_wrap(.~param, scales="free", ncol = 3,
#                 labeller = labeller(param = label_wrap_gen(15)))+
      theme(legend.position="top",
            legend.text=element_text(size=5),
            legend.title = element_blank(),
            plot.margin=margin(20,20,20,0,"pt"),
            text=element_text(size=5)
      )
  }

print(datetime(datax()))
print(summaryPlot(trendbyinterval("hour")))
