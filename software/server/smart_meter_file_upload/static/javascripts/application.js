/*
# * Copyright (c) 2012, Indraprastha Institute of Information Technology,
# * Delhi (IIIT-D) and The Regents of the University of California.
# * All rights reserved.
# *
# * Redistribution and use in source and binary forms, with or without
# * modification, are permitted provided that the following conditions
# * are met:
# * 1. Redistributions of source code must retain the above copyright
# * notice, this list of conditions and the following disclaimer.
# * 2. Redistributions in binary form must reproduce the above
# * copyright notice, this list of conditions and the following
# * disclaimer in the documentation and/or other materials provided
# * with the distribution.
# * 3. Neither the names of the Indraprastha Institute of Information
# * Technology, Delhi and the University of California nor the names
# * of their contributors may be used to endorse or promote products
# * derived from this software without specific prior written permission.
# *
# * THIS SOFTWARE IS PROVIDED BY THE IIIT-D, THE REGENTS, AND CONTRIBUTORS
# * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE IIITD-D, THE REGENTS
# * OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# * SUCH DAMAGE.
# *
# *
#-------------------------------------------------------------------------------
*/
$(".forms").hide();
$("ul li a").click(function(){
	var idToShow = $(this).attr("href");
	$(idToShow).show().siblings(".forms").hide();
	return false;
});
*/
$("#sign_up_confirmation").keyup(function(){
	if( $(this).val() != $("#sign_up_password").val() ) {
		$(this).addClass("error").next().text("Passwords don't match.");
	} else {
		$(this).removeClass("error").next().text("");				
	}
});
