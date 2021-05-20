<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"> 
<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" omit-xml-declaration="yes"/>
<xsl:template match="host">&lt;host&gt;<xsl:value-of select="./@name"/>&lt;host&gt;</xsl:template> 
</xsl:stylesheet>
