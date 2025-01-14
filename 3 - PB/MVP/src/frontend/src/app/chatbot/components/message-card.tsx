import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronRightIcon, Copy } from "lucide-react";

import { formatDate } from 'date-fns';
import { Message } from "@/types/types";
import Link from "next/link";

interface MessageCardProps {
    message: Message
}

export function MessageCard({ message }: MessageCardProps) {

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text)
    }

    return (
        <div className="pb-4">
            <div className={`flex gap-2 ${message.sender === "USER" ? "flex-row-reverse" : ""}`}>
                <Card className={`text-sm flex flex-col max-w-[80%] border-none px-4 py-3 ${message.sender === "USER" ? "bg-primary" : "bg-muted"}`}>
                    <CardContent className="p-0 break-words">
                        <p className={`word-break ${message.sender === "USER" ? "text-primary-foreground" : "text-secondary-foreground"}`}>
                            {message.content}
                        </p>
                    </CardContent>
                    {
                        message.sender === "CHATBOT" && message.relevantDocuments && message.relevantDocuments?.length > 0 && (
                            <CardFooter className="flex-col items-start w-full p-0 mt-4 space-y-2">
                                {
                                    message.relevantDocuments.map((relevantDocument, index) => (
                                        <div key={index} className="flex w-full items-stretch justify-between space-x-2">
                                            <div className="flex flex-grow shadow-md items-center rounded-md bg-card px-4 min-w-0">
                                                <p className="truncate text-xs">
                                                    {relevantDocument}
                                                </p>
                                            </div>
                                            <Button size="sm" className="bg-card shadow-md text-primary hover:text-secondary flex items-center justify-center gap-x-2">
                                                <Link href={`/documents/${relevantDocument}`}>
                                                    <ChevronRightIcon className="w-4 h-4" />
                                                </Link>
                                            </Button>
                                        </div>
                                    ))
                                }
                            </CardFooter>
                        )
                    }
                </Card>
                <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => {
                        copyToClipboard(message.content);
                    }}
                >
                    <Copy className="h-4 w-4" />
                    <span className="sr-only">Copy</span>
                </Button>
            </div>
            <div className={`text-xs mt-2 ${message.sender === "USER" ? "float-right mr-2" : "ml-2"}`}>
                {formatDate(message.timestamp, "dd MMM HH:mm")}
            </div>
        </div>
    )
}