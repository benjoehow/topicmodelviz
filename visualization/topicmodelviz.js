var width = $(window).width()-15,
    barHeight = 60, height = $(window).height()-15;

var x = d3.scale.linear()
    .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width);
    
var hoverColor = "#293A74";
var noHoverColor = "#46C4F3"

function homepage() {
	d3.select("svg").text('');

	chart.attr("height", height);
	var elem = chart.selectAll("circle")
 	   .data(["Topic View"]).enter();

       elem.append("circle")
			.attr("r", 30)
      	 	.attr("cx", 7*width/8)
       		.attr("cy", 7*height/8)
       		.on("click", function(){window.location = "topicoverviewdoc.html"})
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
 	        
 	  elem.append("text")
       		.attr("x", 7*width/8)
     		.attr("y", 7*height/8+5)
     		.attr("href", "topicoverviewdoc.html")
     		.on("click", function(){window.location = "topicoverviewdoc.html"})
       		.style("font-size","20px")
       		.style("cursor", "pointer")
       		.text("HALP");
       		
d3.json("json/topics.json", function(data) {
	var order = data.order;
	var topics = data.topics;
	
	x.domain([0, d3.max(topics, function(d) { return d.prev; })]);
	

	
 	 var bar = chart.selectAll("g")
 	     .data(topics)
 	     .enter().append("g")
 	     .style("fill", noHoverColor)
 	     .on("mouseover", function(){d3.select(this).style("fill", hoverColor)})
 	     .on("mouseout", function(){ d3.select(this).style("fill", noHoverColor)})
     	 .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

 	 bar.append("rect")
   		   .attr("width", function(d) { return width*(d.prev); })
   		   .attr("height", barHeight - 10)
   		   .on("click", function(d){topicviz(d.id)})
   		   .attr("x", function(d) {return width/2-(width*(d.prev)/2)});

 	 bar.append("text")
     	 .attr("x", function(d) { return width/2; })
     	 .attr("y", barHeight / 2)
     	 .style("font-size","20px")
     	 .style("cursor", "pointer")
     	 .on("click", function(d){topicviz(d.id)})
      	 .text(function(d) {
      	 	var allWords = d.words.split(' ');
      	 	var first3Words = [];
      	 	for(var i = 0; i < 3; i++){
      	 		first3Words.push(allWords[i])
      	 	}
      	 return first3Words; });

});
}


function topicviz(id) {
		d3.select("svg").text('');
		x.domain([0, 400]);
		chart.attr("height", height);
		
		var elem = chart.selectAll("circle")
 	     .data(["Topic View"]).enter();
 	     
 	     elem.append("circle")
			.attr("r", 45)
      	 	.attr("cx", width/8)
       		.attr("cy", 60)
       		.on("click", homepage)
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
       		
       	elem.append("text")
       		.attr("x", width/8)
     		.attr("y", 60)
       		.style("font-size","16px")
       		.on("click", homepage)
       		.style("cursor", "pointer")
       		.text(function(d){return d});
       		
       	elem.append("circle")
			.attr("r", 30)
      	 	.attr("cx", 7*width/8)
       		.attr("cy", 7*height/8)
       		.on("click", function(){window.location = "topicdetaildoc.html"})
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
 	        
 	   elem.append("text")
       		.attr("x", 7*width/8)
     		.attr("y", 7*height/8+5)
     		.attr("href", "topicoverviewdoc.html")
     		.on("click", function(){window.location = "topicdetaildoc.html"})
       		.style("font-size","20px")
       		.style("cursor", "pointer")
       		.text("HALP");

       		
       	d3.json("json/topics/topic_" + id + ".json", function(data) {
       	
       			
			var words = data.words;
			
			var first3Words = [];
      	 		for(var i = 0; i < 3; i++){
      	 			first3Words.push(words[i].word)
      	 		}
      	 		
      	 	elem.append("text")
       			.attr("x", width/2)
       			.attr("y", 65)
       			.style("font-size","30px")
       			.text(first3Words);
			
			var bars = chart.selectAll("words")
 	     		.data(words)
 	    		.enter().append("g")
 			    .style("fill", noHoverColor)
     	 		.attr("transform", function(d, i) { return "translate(0," + i * 5*barHeight/7 + ")"; });
     	 		
     	 	bars.append("rect")
     	 			.attr("width", function(d) { return (width/6)*(d.prev); })
   			  	    .attr("height", (barHeight - 25)/2)
   			   		.attr("y", 170);
   		   			
   		   	bars.append("text")
   		   			.attr("y", 165)
     	 			.style("font-size","20px")
     	 			.style("text-anchor", "start")
     	 			.style("cursor", "pointer")
   		   			.text(function(d){ return d.word;});
   		   			
   		    var docs = chart.selectAll("docs")
   		    	.data(data.documents)
   		   		.enter().append("g")
 			    .style("fill", noHoverColor)
 			    .on("mouseover", function(){d3.select(this).style("fill", hoverColor)})
 			    .on("mouseout", function(){ d3.select(this).style("fill", noHoverColor)})
   		   		.attr("transform", function(d, i) { return "translate(0," + i * 40 + ")"; });	
   		   		
   		     docs.append("rect")
   		   		.attr('x', function(d){return width/2-d.weight*width/4})
   		   		.attr('y', 150)
   		   		.attr("width", function(d){return d.weight*width/2})
   		   		.attr("height", 40)
   		   		.on("click", function(d){
   		   			docviz(d.docid);
   		   		});;
   		   	
   		   		
   		   	docs.append("text")
   		   		.attr("x", width/2)
   		   		.attr("y", 175)
   		   		.style("font-size","25px")
   		   		.style("cursor", "pointer")
   		   		.text(function(d){ return d.docid;})
   		   		.on("click", function(d){
   		   			docviz(d.docid);
   		   		});
   		   		
   	/*	elem.append("circle")
			.attr("r", 30)
      	 	.attr("cx", 7*width/8)
       		.attr("cy", 170)
       		.on("click", reOrder)
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
 	        
 	   elem.append("text")
       		.attr("x", 7*width/8)
     		.attr("y", 175)
     		.attr("href", "topicoverviewdoc.html")
     		.on("click", reOrder)
       		.style("font-size","20px")
       		.style("cursor", "pointer")
       		.text("HALP");
   		   		
   		   	
   		   		
   		   	reOrder = setInterval(function() {
 
				docs.sort(function(a, b) { return a.relev - b.relev; });
	 
				docs.transition()
					.duration(750)
					.delay(function(d, i) { return i * 50; })
					.attr("transform", function(d, i) { return "translate(0," + 10 + ")"; });
	 
				}, 5000) */
				       			
       	
       	});		
}

function docviz(docid) {
	d3.select("svg").text('');
	
	var elem = chart.selectAll("circle")
 	     .data(["Topic View"]).enter();
 	     
 	     elem.append("circle")
			.attr("r", 45)
      	 	.attr("cx", width/8)
       		.attr("cy", 60)
       		.on("click", homepage)
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
       		
       	elem.append("text")
       		.attr("x", width/8)
     		.attr("y", 60)
       		.style("font-size","16px")
       		.on("click", homepage)
       		.style("cursor", "pointer")
       		.text(function(d){return d});
       		
       elem.append("circle")
			.attr("r", 30)
      	 	.attr("cx", 7*width/8)
       		.attr("cy", 7*height/8)
       		.on("click", function(){window.location = "documentdetaildoc.html"})
       		.style("fill", "#46C4F3")
 	     	.on("mouseover", function(){d3.select(this).style("fill", "#293A74")})
 	        .on("mouseout", function(){d3.select(this).style("fill", "#46C4F3")});
 	        
 	   elem.append("text")
       		.attr("x", 7*width/8)
     		.attr("y", 7*height/8+5)
     		.attr("href", "topicoverviewdoc.html")
     		.on("click", function(){window.location = "documentdetaildoc.html"})
       		.style("font-size","20px")
       		.style("cursor", "pointer")
       		.text("HALP");
       		
       	elem.append("text")
       		.attr("x", width/2)
       		.attr("y", 65)
       		.style("font-size","30px")
       		.text(docid);
       		
       		
       	d3.json("json/documents/" + docid + ".json", function(data) {
       		var topics = data.topics
       		
       		x.domain([0, d3.max(data.topics, function(d) { return d.prev; })]);
       		chart.attr("height", height);
			
			var elem = chart.selectAll("g")
 	 			.data(topics)
 	   			.enter().append("g")
 			    .style("fill", noHoverColor)
 			    .on("mouseover", function(){d3.select(this).style("fill", hoverColor)})
 			    .on("mouseout", function(){ d3.select(this).style("fill", noHoverColor)})
     			.attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

 			elem.append("rect")
   			   .attr("width", function(d) { return (width/4)*(d.prev); })
   			   .attr("height", barHeight - 25)
   			   .attr("y", 170)
   			   .on("click", function(d){
   			  	 topicviz(d.id);
   			   });
   			   
 	   			
 	   		elem.append("text")
     			.attr("y", 165)
     	 		.style("font-size","20px")
     	 		.style("text-anchor", "start")
     	 		.style("cursor", "pointer")
     	 		.on("click", function(d){
   			  		topicviz(d.id);
   			   	})
      			 .text(function(d) {
      			 	var allWords = d.words.split(' ');
      			 	var first3Words = [];
      			 	for(var i = 0; i < 3; i++){
      			 		first3Words.push(allWords[i])
      			 	}
     		 	 return first3Words; });
     		 	 
			var svg = d3.select("svg").data(data.content);
 
svg.append("foreignObject")
	.attr("x", 4*width/14)
	.attr("y", 150)
	.attr("width", 2*width/3-50)
	.attr("height", 7*height/10)
	.style("color", "white")
	.append("xhtml:body")
	.style("font", "14px 'Helvetica Neue'")
	.html(data.content);
			//var bars = chart.selectAll("g")
 	     		/*.data(data.content)
 	    		.enter().append("g")
     	 		.attr("transform", function(d, i) { return "translate(0," + i * 15 + ")"; });
   		   		
   		   		
   		    	.data(data.topics)
   		   		.enter().append("g")
   		   		.attr("transform", function(d, i) { return "translate(0," + i * 150 + ")"; });	
   		   		
   		   	elem.append("rect")
   		   		.attr("width", function(d) { return 200*(d.prev); })
   		   		.attr("height", 10)
   		   		.attr("x", function(d) {return width/2-(width*(d.prev)/2)})
   		   		.attr("y", 200)
   		   		.on("click", function(d) {alert(d.prev)});
   		   		
   		    	bars.append("text")
   		   		.attr("x", 800)
   		   		.attr("y", 110)
   		   		.style("text-anchor", "start")
   		   		.style("font-size","16px")
   		   		.text(function(d){return d});*/
   		   	
       	});		

}