<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"> 
<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" omit-xml-declaration="yes"/>
<xsl:template match="host">&lt;host name="<xsl:value-of select="./@name"/>" status="<xsl:value-of select="status"/>"/&gt;</xsl:template> 
</xsl:stylesheet>
